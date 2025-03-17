import tkinter as tk
from tkinter import ttk
import re
from datetime import datetime
import os
import random
import string
from PIL import Image, ImageTk

class FormValidator:
    """Utility class to handle form validation"""
    
    @staticmethod
    def validate_email(email):
        """Validate an email address"""
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_phone(phone):
        """Validate a phone number (numeric only)"""
        return phone.isdigit()
    
    @staticmethod
    def validate_number(value):
        """Validate if a string is a valid number"""
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_date(date_str, format='%Y-%m-%d'):
        """Validate if a string is a valid date"""
        try:
            datetime.strptime(date_str, format)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def calculate_age(birth_date, format='%Y-%m-%d'):
        """Calculate age from birth date"""
        birth_date = datetime.strptime(birth_date, format)
        today = datetime.now()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age

class UIHelper:
    """Helper class for UI-related functions"""
    
    @staticmethod
    def create_rounded_frame(parent, width, height, bg_color, radius=20):
        """Create a rounded corner frame"""
        # Not directly possible in Tkinter, this is a workaround using Canvas
        frame = tk.Frame(parent, width=width, height=height, bg=parent["bg"])
        canvas = tk.Canvas(frame, width=width, height=height, bg=parent["bg"], highlightthickness=0)
        canvas.pack()
        
        # Top left corner
        canvas.create_arc((0, 0, radius*2, radius*2), start=90, extent=90, fill=bg_color, outline=bg_color)
        # Top right corner
        canvas.create_arc((width-radius*2-2, 0, width, radius*2), start=0, extent=90, fill=bg_color, outline=bg_color)
        # Bottom left corner
        canvas.create_arc((0, height-radius*2-2, radius*2, height), start=180, extent=90, fill=bg_color, outline=bg_color)
        # Bottom right corner
        canvas.create_arc((width-radius*2-2, height-radius*2-2, width, height), start=270, extent=90, fill=bg_color, outline=bg_color)
        
        # Rectangles to fill in the sides
        canvas.create_rectangle((radius, 0, width-radius, height), fill=bg_color, outline=bg_color)
        canvas.create_rectangle((0, radius, width, height-radius), fill=bg_color, outline=bg_color)
        
        return frame
    
    @staticmethod
    def load_and_resize_image(image_path, width, height):
        """Load and resize an image for tkinter"""
        try:
            if os.path.exists(image_path):
                image = Image.open(image_path)
                image = image.resize((width, height), Image.LANCZOS)
                return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
        return None
    
    @staticmethod
    def center_window(window, width, height):
        """Center a window on the screen"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    @staticmethod
    def add_hover_effect(widget, normal_bg, hover_bg):
        """Add hover effect to a widget"""
        widget.bind("<Enter>", lambda e: widget.configure(background=hover_bg))
        widget.bind("<Leave>", lambda e: widget.configure(background=normal_bg))

class ReportGenerator:
    """Class to generate PDF and Excel reports"""
    
    @staticmethod
    def generate_student_report(db, output_path="reports"):
        """Generate a student report CSV file"""
        import csv
        from datetime import datetime
        
        # Create reports directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(output_path, f"student_report_{timestamp}.csv")
        
        try:
            # Get all student registration numbers
            reg_numbers = db.get_all_student_reg_numbers()
            
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                # Write header
                writer.writerow(['Reg No', 'First Name', 'Last Name', 'Date of Birth', 
                              'Gender', 'Email', 'Mobile Phone', 'Parent Name', 'NIC'])
                
                # Write data for each student
                for reg_no in reg_numbers:
                    student = db.get_student_by_reg_no(reg_no)
                    if student:
                        writer.writerow([
                            student['regNo'],
                            student['firstName'],
                            student['lastName'],
                            student['dateOfBirth'],
                            student['gender'],
                            student['email'],
                            student['mobilePhone'],
                            student['parentName'],
                            student['nic']
                        ])
            
            return filename
        except Exception as e:
            print(f"Error generating student report: {e}")
            return None
    
    @staticmethod
    def generate_teacher_report(db, output_path="reports"):
        """Generate a teacher report CSV file"""
        import csv
        from datetime import datetime
        
        # Create reports directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(output_path, f"teacher_report_{timestamp}.csv")
        
        try:
            # Get all teacher registration numbers
            reg_numbers = db.get_all_teacher_reg_numbers()
            
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                # Write header
                writer.writerow(['Reg No', 'First Name', 'Last Name', 'Date of Birth', 
                              'Gender', 'Email', 'Mobile Phone', 'Specialization', 'Salary'])
                
                # Write data for each teacher
                for reg_no in reg_numbers:
                    teacher = db.get_teacher_by_reg_no(reg_no)
                    if teacher:
                        writer.writerow([
                            teacher['regNo'],
                            teacher['firstName'],
                            teacher['lastName'],
                            teacher['dateOfBirth'],
                            teacher['gender'],
                            teacher['email'],
                            teacher['mobilePhone'],
                            teacher['specialization'],
                            teacher['salary']
                        ])
            
            return filename
        except Exception as e:
            print(f"Error generating teacher report: {e}")
            return None

class DatabaseBackup:
    """Class to handle database backup and restore"""
    
    @staticmethod
    def backup_database(source_path="database/edupro.db", backup_dir="backups"):
        """Create a backup of the database"""
        import shutil
        from datetime import datetime
        
        # Create backup directory if it doesn't exist
        os.makedirs(backup_dir, exist_ok=True)
        
        # Generate backup filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = os.path.join(backup_dir, f"edupro_backup_{timestamp}.db")
        
        try:
            shutil.copy2(source_path, backup_path)
            return backup_path
        except Exception as e:
            print(f"Error backing up database: {e}")
            return None
    
    @staticmethod
    def restore_database(backup_path, target_path="database/edupro.db"):
        """Restore database from backup"""
        import shutil
        
        try:
            shutil.copy2(backup_path, target_path)
            return True
        except Exception as e:
            print(f"Error restoring database: {e}")
            return False

class DemoDataGenerator:
    """Class to generate demo data for testing"""
    
    @staticmethod
    def generate_demo_data(db, num_students=10, num_teachers=5):
        """Generate demo data for students and teachers"""
        # Generate students
        for _ in range(num_students):
            student = DemoDataGenerator._generate_random_student()
            db.insert_student(student)
        
        # Generate teachers
        for _ in range(num_teachers):
            teacher = DemoDataGenerator._generate_random_teacher()
            db.insert_teacher(teacher)
        
        return True
    
    @staticmethod
    def _generate_random_student():
        """Generate random student data"""
        # First names
        first_names = ["John", "Emma", "Michael", "Sophia", "William", "Olivia", 
                      "James", "Ava", "Alexander", "Isabella", "Ethan", "Mia", 
                      "Daniel", "Charlotte", "Matthew", "Amelia", "Aiden", "Emily"]
        
        # Last names
        last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", 
                     "Miller", "Wilson", "Moore", "Taylor", "Anderson", "Thomas", 
                     "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia"]
        
        # Random date of birth (between 10 and 18 years ago)
        year = random.randint(datetime.now().year - 18, datetime.now().year - 10)
        month = random.randint(1, 12)
        day = random.randint(1, 28)  # To avoid potential month-end issues
        date_of_birth = f"{year}-{month:02d}-{day:02d}"
        
        # Generate random NIC (simple format for demo)
        nic = ''.join(random.choices(string.digits, k=9))
        
        return {
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
    
    @staticmethod
    def _generate_random_teacher():
        """Generate random teacher data"""
        # First names
        first_names = ["Robert", "Mary", "David", "Jennifer", "Joseph", "Patricia", 
                      "Charles", "Linda", "Thomas", "Elizabeth", "Christopher", "Susan", 
                      "Richard", "Jessica", "Daniel", "Sarah", "Matthew", "Karen"]
        
        # Last names
        last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", 
                     "Miller", "Wilson", "Moore", "Taylor", "Anderson", "Thomas", 
                     "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia"]
        
        # Specializations
        specializations = ["Mathematics", "Science", "English", "History", "Geography",
                         "Computer Science", "Physics", "Chemistry", "Biology", 
                         "Art", "Music", "Physical Education", "Foreign Languages"]
        
        # Random date of birth (between 25 and 60 years ago)
        year = random.randint(datetime.now().year - 60, datetime.now().year - 25)
        month = random.randint(1, 12)
        day = random.randint(1, 28)  # To avoid potential month-end issues
        date_of_birth = f"{year}-{month:02d}-{day:02d}"
        
        # Generate random NIC (simple format for demo)
        nic = ''.join(random.choices(string.digits, k=9))
        
        # Random salary between 30000 and 90000
        salary = random.randint(30000, 90000)
        
        return {
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