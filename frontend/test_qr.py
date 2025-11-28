import qrcode
import os

def test_qr_generation():
    print("Testing QR Code Generation...")
    print("=" * 50)
    
    qr_dir = "../qr_codes"
    os.makedirs(qr_dir, exist_ok=True)
    print(f"✓ QR codes directory: {os.path.abspath(qr_dir)}")
    
    test_students = [
        {"code": "24-49051", "name": "John Doe"},
        {"code": "24-49052", "name": "Jane Smith"},
        {"code": "24-49053", "name": "Bob Johnson"}
    ]
    
    print(f"\nGenerating QR codes for {len(test_students)} test students...")
    
    for student in test_students:
        student_code = student['code']
        student_name = student['name']
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(student_code)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        filename = f"{student_code.replace('-', '_')}.png"
        filepath = os.path.join(qr_dir, filename)
        img.save(filepath)
        
        print(f"✓ Generated: {filename} for {student_name} ({student_code})")
    
    print("\n" + "=" * 50)
    print("QR Code generation test completed successfully!")
    print(f"QR codes saved in: {os.path.abspath(qr_dir)}")
    print("\nYou can now:")
    print("1. View the generated QR codes in the qr_codes folder")
    print("2. Test scanning them with your phone's camera")
    print("3. Use them in the EduCore application")

if __name__ == "__main__":
    try:
        test_qr_generation()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure qrcode package is installed: pip install qrcode[pil]")
