"""
Generate QR Codes for Existing Students
Run this script to generate QR codes for all students already in the database
"""
import requests
import qrcode
import os
import sys

def generate_qr_codes_for_existing_students():
    """Generate QR codes for all existing students in the database"""
    print("=" * 60)
    print("  Generate QR Codes for Existing Students")
    print("=" * 60)
    print()
    
    # API endpoint
    API_URL = "http://localhost:8000/api/students"
    
    # QR codes directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    qr_dir = os.path.join(os.path.dirname(script_dir), "qr_codes")
    os.makedirs(qr_dir, exist_ok=True)
    
    print(f"QR codes will be saved to: {qr_dir}")
    print()
    
    try:
        # Fetch all students
        print("Fetching students from backend...")
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        students = response.json()
        
        if not students:
            print("No students found in the database.")
            print("Add some students first, then run this script again.")
            return
        
        print(f"Found {len(students)} students in the database.")
        print()
        print("Generating QR codes...")
        print("-" * 60)
        
        success_count = 0
        skip_count = 0
        error_count = 0
        
        for student in students:
            student_code = student['student_code']
            student_name = student['name']
            
            # Check if QR code already exists
            filename = f"{student_code.replace('-', '_')}.png"
            filepath = os.path.join(qr_dir, filename)
            
            if os.path.exists(filepath):
                print(f"[SKIP] {student_code} - {student_name} (QR code already exists)")
                skip_count += 1
                continue
            
            try:
                # Create QR code
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(student_code)
                qr.make(fit=True)
                
                # Create and save image
                img = qr.make_image(fill_color="black", back_color="white")
                img.save(filepath)
                
                print(f"[OK]   {student_code} - {student_name}")
                success_count += 1
                
            except Exception as e:
                print(f"[ERROR] {student_code} - {student_name}: {str(e)}")
                error_count += 1
        
        print("-" * 60)
        print()
        print("Summary:")
        print(f"  Total students: {len(students)}")
        print(f"  QR codes generated: {success_count}")
        print(f"  Already existed: {skip_count}")
        print(f"  Errors: {error_count}")
        print()
        
        if success_count > 0:
            print(f"Success! Generated {success_count} new QR code(s).")
            print(f"QR codes saved in: {qr_dir}")
        else:
            print("No new QR codes generated.")
            if skip_count > 0:
                print("All students already have QR codes!")
        
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to backend server.")
        print("Make sure the backend is running on http://localhost:8000")
        print()
        print("To start the backend:")
        print("  cd backend")
        print("  python main.py")
        sys.exit(1)
        
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Failed to fetch students from API: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        sys.exit(1)
    
    print()
    print("=" * 60)
    print("Done!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        generate_qr_codes_for_existing_students()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
