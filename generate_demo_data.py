import os
import sys
import argparse
from database import Database
from utilities import DemoDataGenerator

def main():
    """
    Generate demo data for the EduPro Academy system.
    This script creates sample students and teachers for testing purposes.
    """
    
    # Set up command line arguments
    parser = argparse.ArgumentParser(description='Generate demo data for EduPro Academy')
    parser.add_argument('--students', type=int, default=20,
                       help='Number of student records to generate (default: 20)')
    parser.add_argument('--teachers', type=int, default=10,
                       help='Number of teacher records to generate (default: 10)')
    parser.add_argument('--clear', action='store_true',
                       help='Clear existing data before generating new data')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("     EduPro Academy - Demo Data Generator")
    print("=" * 60)
    
    # Make sure the database directory exists
    os.makedirs('database', exist_ok=True)
    
    # Initialize the database
    db = Database()
    
    if args.clear:
        print("\nClearing existing data...")
        # A more thorough approach would be to delete the database file and recreate it,
        # but for simplicity, we'll just delete all records
        
        # Get all registration numbers
        student_reg_numbers = db.get_all_student_reg_numbers()
        teacher_reg_numbers = db.get_all_teacher_reg_numbers()
        
        # Delete all students
        for reg_no in student_reg_numbers:
            db.delete_student(reg_no)
        
        # Delete all teachers
        for reg_no in teacher_reg_numbers:
            db.delete_teacher(reg_no)
        
        print(f"Cleared {len(student_reg_numbers)} student records and {len(teacher_reg_numbers)} teacher records")
    
    # Generate the demo data
    print(f"\nGenerating {args.students} student records...")
    print(f"Generating {args.teachers} teacher records...\n")
    
    try:
        result = DemoDataGenerator.generate_demo_data(db, args.students, args.teachers)
        
        if result:
            # Count the actual records created
            student_count = len(db.get_all_student_reg_numbers())
            teacher_count = len(db.get_all_teacher_reg_numbers())
            
            print("\nDemo data generation completed successfully!")
            print(f"- {student_count} student records in database")
            print(f"- {teacher_count} teacher records in database")
            print("\nYou can now log in with the following credentials:")
            print("Username: admin")
            print("Password: 1234")
        else:
            print("\nError generating demo data. Please check the error logs.")
    except Exception as e:
        print(f"\nError: {e}")
        print("Demo data generation failed.")
    
    # Close the database connection
    db.close()
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()