import os
import sys
import argparse
import random
import string
from datetime import datetime
from database import Database

class DemoDataGenerator:
    def __init__(self, db):
        self.db = db
    
    def generate_data(self, num_students=20, num_teachers=10):
        self._generate_students(num_students)
        self._generate_teachers(num_teachers)
        return True
    
    def _generate_students(self, count):
        first_names = ["John", "Emma", "Michael", "Sophia", "William", "Olivia", 
                      "James", "Ava", "Alexander", "Isabella", "Ethan", "Mia", 
                      "Daniel", "Charlotte", "Matthew", "Amelia", "Aiden", "Emily"]
        
        last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", 
                     "Miller", "Wilson", "Moore", "Taylor", "Anderson", "Thomas", 
                     "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia"]
        
        for _ in range(count):
            year = random.randint(datetime.now().year - 18, datetime.now().year - 10)
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            date_of_birth = f"{year}-{month:02d}-{day:02d}"
            
            nic = ''.join(random.choices(string.digits, k=9))
            
            student_data = {
                'firstName': random.choice(first_names),
                'lastName': random.choice(last_names),
                'dateOfBirth': date_of_birth,
                'gender': random.choice(["Male", "Female"]),
                'address': f"{random.randint(1, 999)} Main Street, City",
                'email': f"student{random.randint(100, 999)}@example.com",
                'mobilePhone': ''.join(random.choices(string.digits, k=10)),
                'homePhone': ''.join(random.choices(string.digits, k=10)),
                'parentName': f"{random.choice(first_names)} {random.choice(last_names)}",
                'nic': nic,
                'contactNo': ''.join(random.choices(string.digits, k=10))
            }
            
            self.db.insert_student(student_data)
    
    def _generate_teachers(self, count):
        first_names = ["Robert", "Mary", "David", "Jennifer", "Joseph", "Patricia", 
                      "Charles", "Linda", "Thomas", "Elizabeth", "Christopher", "Susan", 
                      "Richard", "Jessica", "Daniel", "Sarah", "Matthew", "Karen"]
        
        last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", 
                     "Miller", "Wilson", "Moore", "Taylor", "Anderson", "Thomas", 
                     "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia"]
        
        specializations = ["Mathematics", "Science", "English", "History", "Geography",
                         "Computer Science", "Physics", "Chemistry", "Biology", 
                         "Art", "Music", "Physical Education", "Foreign Languages"]
        
        for _ in range(count):
            year = random.randint(datetime.now().year - 60, datetime.now().year - 25)
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            date_of_birth = f"{year}-{month:02d}-{day:02d}"
            
            nic = ''.join(random.choices(string.digits, k=9))
            
            salary = random.randint(30000, 90000)
            
            teacher_data = {
                'firstName': random.choice(first_names),
                'lastName': random.choice(last_names),
                'dateOfBirth': date_of_birth,
                'gender': random.choice(["Male", "Female"]),
                'address': f"{random.randint(1, 999)} Main Street, City",
                'email': f"teacher{random.randint(100, 999)}@example.com",
                'mobilePhone': ''.join(random.choices(string.digits, k=10)),
                'homePhone': ''.join(random.choices(string.digits, k=10)),
                'specialization': random.choice(specializations),
                'nic': nic,
                'salary': salary
            }
            
            self.db.insert_teacher(teacher_data)

def main():
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
    
    os.makedirs('database', exist_ok=True)
    
    db = Database()
    
    if args.clear:
        print("\nClearing existing data...")
        
        student_reg_numbers = db.get_all_student_reg_numbers()
        teacher_reg_numbers = db.get_all_teacher_reg_numbers()
        
        for reg_no in student_reg_numbers:
            db.delete_student(reg_no)
        
        for reg_no in teacher_reg_numbers:
            db.delete_teacher(reg_no)
        
        print(f"Cleared {len(student_reg_numbers)} student records and {len(teacher_reg_numbers)} teacher records")
    
    print(f"\nGenerating {args.students} student records...")
    print(f"Generating {args.teachers} teacher records...\n")
    
    try:
        generator = DemoDataGenerator(db)
        result = generator.generate_data(args.students, args.teachers)
        
        if result:
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
    
    db.close()
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()