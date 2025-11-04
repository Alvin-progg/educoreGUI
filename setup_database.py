"""
Database setup script for EduCore
Creates database and tables if they don't exist
"""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def create_database():
    """Create database if it doesn't exist"""
    try:
        # Connect without specifying database
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '')
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            db_name = os.getenv('DB_NAME', 'educore_db')
            
            # Create database
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✓ Database '{db_name}' created or already exists")
            
            cursor.close()
            connection.close()
            return True
            
    except Error as e:
        print(f"✗ Error creating database: {e}")
        return False

def test_connection():
    """Test database connection"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'educore_db'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '')
        )
        
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"✓ Successfully connected to MySQL Server version {db_info}")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print(f"✓ Connected to database: {record[0]}")
            cursor.close()
            connection.close()
            return True
            
    except Error as e:
        print(f"✗ Error connecting to MySQL: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("  EduCore Database Setup")
    print("=" * 60)
    print()
    
    if not os.path.exists('.env'):
        print("✗ .env file not found!")
        print("  Please copy .env.example to .env and configure your database credentials")
        exit(1)
    
    print("Step 1: Creating database...")
    if create_database():
        print()
        print("Step 2: Testing connection...")
        if test_connection():
            print()
            print("=" * 60)
            print("✓ Database setup completed successfully!")
            print("=" * 60)
            print()
            print("Next steps:")
            print("1. Run the backend server: cd backend && python main.py")
            print("2. Tables will be created automatically on first run")
            print("3. Then run the GUI: cd frontend && python gui.py")
        else:
            print()
            print("✗ Connection test failed. Please check your .env configuration")
    else:
        print()
        print("✗ Database creation failed. Please check your MySQL server and credentials")
