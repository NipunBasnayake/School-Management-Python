import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self):
        os.makedirs('database', exist_ok=True)
        self.conn = sqlite3.connect('database/edupro.db')
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.update_schema() # Add schema upgrade function
    
    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Students (
            regNo INTEGER PRIMARY KEY AUTOINCREMENT,
            firstName VARCHAR(50) NOT NULL,
            lastName VARCHAR(50) NOT NULL,
            dateOfBirth DATE NOT NULL,
            gender VARCHAR(50) NOT NULL,
            address VARCHAR(100) NOT NULL,
            email VARCHAR(50) NOT NULL,
            mobilePhone INTEGER NOT NULL,
            homePhone INTEGER,
            parentName VARCHAR(50) NOT NULL,
            nic VARCHAR(50) NOT NULL UNIQUE,
            contactNo INTEGER NOT NULL
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Teachers (
            regNo INTEGER PRIMARY KEY AUTOINCREMENT,
            firstName VARCHAR(50) NOT NULL,
            lastName VARCHAR(50) NOT NULL,
            dateOfBirth DATE NOT NULL,
            gender VARCHAR(50) NOT NULL,
            address VARCHAR(100) NOT NULL,
            email VARCHAR(50) NOT NULL,
            mobilePhone INTEGER NOT NULL,
            homePhone INTEGER,
            specialization VARCHAR(50) NOT NULL,
            nic VARCHAR(50) NOT NULL UNIQUE,
            salary REAL NOT NULL
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            username VARCHAR(50) PRIMARY KEY,
            password VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_type VARCHAR(20) DEFAULT 'staff'
        )
        ''')
        
        self.cursor.execute("SELECT COUNT(*) FROM Users WHERE username = 'admin'")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute("INSERT INTO Users (username, password, user_type) VALUES ('admin', '1234', 'admin')")
        
        self.conn.commit()
    
    def update_schema(self):
        """Update database schema if needed"""
        try:
            # Check if last_login column exists in Users table
            self.cursor.execute("PRAGMA table_info(Users)")
            columns = [col[1] for col in self.cursor.fetchall()]
            
            # Add last_login column if it doesn't exist
            if 'last_login' not in columns:
                self.cursor.execute("ALTER TABLE Users ADD COLUMN last_login TIMESTAMP")
                self.conn.commit()
                print("Database schema updated: Added last_login column to Users table")
            
            # Add other schema updates here as needed
                
        except Exception as e:
            print(f"Error updating schema: {e}")
    
    def verify_login(self, username, password):
        try:
            # First check if the user exists
            self.cursor.execute("SELECT * FROM Users WHERE username=? AND password=?", 
                            (username, password))
            user = self.cursor.fetchone()
            
            if user:
                try:
                    # Try to update the last login time, but don't fail if column doesn't exist
                    self.cursor.execute("UPDATE Users SET last_login = ? WHERE username = ?", 
                                    (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), username))
                    self.conn.commit()
                except sqlite3.OperationalError:
                    # If the column doesn't exist, just ignore the error
                    pass
                
                return True
            return False
        except Exception as e:
            print(f"Login verification error: {e}")
            return False
    
    def check_username_exists(self, username):
        self.cursor.execute("SELECT COUNT(*) FROM Users WHERE username=?", (username,))
        return self.cursor.fetchone()[0] > 0
    
    def create_user(self, username, password, user_type='staff'):
        try:
            if self.check_username_exists(username):
                return False
            
            self.cursor.execute("INSERT INTO Users (username, password, user_type) VALUES (?, ?, ?)", 
                              (username, password, user_type))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
    
    def get_user_type(self, username):
        self.cursor.execute("SELECT user_type FROM Users WHERE username=?", (username,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None
    
    def insert_student(self, student_data):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM Students WHERE nic=?", 
                               (student_data['nic'],))
            if self.cursor.fetchone()[0] > 0:
                return False
            
            query = '''
            INSERT INTO Students 
            (firstName, lastName, dateOfBirth, gender, address, email, 
             mobilePhone, homePhone, parentName, nic, contactNo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            
            self.cursor.execute(query, (
                student_data['firstName'],
                student_data['lastName'],
                student_data['dateOfBirth'],
                student_data['gender'],
                student_data['address'],
                student_data['email'],
                student_data['mobilePhone'],
                student_data['homePhone'] if student_data['homePhone'] else None,
                student_data['parentName'],
                student_data['nic'],
                student_data['contactNo']
            ))
            
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error inserting student: {e}")
            return False
    
    def update_student(self, reg_no, student_data):
        try:
            query = '''
            UPDATE Students 
            SET firstName=?, lastName=?, dateOfBirth=?, gender=?, address=?, 
                email=?, mobilePhone=?, homePhone=?, parentName=?, nic=?, contactNo=?
            WHERE regNo=?
            '''
            
            self.cursor.execute(query, (
                student_data['firstName'],
                student_data['lastName'],
                student_data['dateOfBirth'],
                student_data['gender'],
                student_data['address'],
                student_data['email'],
                student_data['mobilePhone'],
                student_data['homePhone'] if student_data['homePhone'] else None,
                student_data['parentName'],
                student_data['nic'],
                student_data['contactNo'],
                reg_no
            ))
            
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating student: {e}")
            return False
    
    def delete_student(self, reg_no):
        try:
            self.cursor.execute("DELETE FROM Students WHERE regNo=?", (reg_no,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting student: {e}")
            return False
    
    def get_all_student_reg_numbers(self):
        self.cursor.execute("SELECT regNo FROM Students ORDER BY regNo")
        return [str(row[0]) for row in self.cursor.fetchall()]
    
    def get_student_by_reg_no(self, reg_no):
        try:
            self.cursor.execute("""
            SELECT regNo, firstName, lastName, dateOfBirth, gender, address, 
                   email, mobilePhone, homePhone, parentName, nic, contactNo 
            FROM Students 
            WHERE regNo=?
            """, (reg_no,))
            
            row = self.cursor.fetchone()
            if row:
                return {
                    'regNo': row[0],
                    'firstName': row[1],
                    'lastName': row[2],
                    'dateOfBirth': row[3],
                    'gender': row[4],
                    'address': row[5],
                    'email': row[6],
                    'mobilePhone': row[7],
                    'homePhone': row[8],
                    'parentName': row[9],
                    'nic': row[10],
                    'contactNo': row[11]
                }
            return None
        except Exception as e:
            print(f"Error retrieving student: {e}")
            return None
    
    def get_students_count(self):
        self.cursor.execute("SELECT COUNT(*) FROM Students")
        return self.cursor.fetchone()[0]
    
    def search_students(self, search_term):
        try:
            query = """
            SELECT regNo, firstName, lastName FROM Students
            WHERE firstName LIKE ? OR lastName LIKE ? OR nic LIKE ?
            ORDER BY firstName, lastName
            LIMIT 50
            """
            search_pattern = f"%{search_term}%"
            self.cursor.execute(query, (search_pattern, search_pattern, search_pattern))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error searching students: {e}")
            return []
    
    def insert_teacher(self, teacher_data):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM Teachers WHERE nic=?", 
                               (teacher_data['nic'],))
            if self.cursor.fetchone()[0] > 0:
                return False
            
            query = '''
            INSERT INTO Teachers 
            (firstName, lastName, dateOfBirth, gender, address, email, 
             mobilePhone, homePhone, specialization, nic, salary)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            
            self.cursor.execute(query, (
                teacher_data['firstName'],
                teacher_data['lastName'],
                teacher_data['dateOfBirth'],
                teacher_data['gender'],
                teacher_data['address'],
                teacher_data['email'],
                teacher_data['mobilePhone'],
                teacher_data['homePhone'] if teacher_data['homePhone'] else None,
                teacher_data['specialization'],
                teacher_data['nic'],
                teacher_data['salary']
            ))
            
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error inserting teacher: {e}")
            return False
    
    def update_teacher(self, reg_no, teacher_data):
        try:
            query = '''
            UPDATE Teachers 
            SET firstName=?, lastName=?, dateOfBirth=?, gender=?, address=?, 
                email=?, mobilePhone=?, homePhone=?, specialization=?, nic=?, salary=?
            WHERE regNo=?
            '''
            
            self.cursor.execute(query, (
                teacher_data['firstName'],
                teacher_data['lastName'],
                teacher_data['dateOfBirth'],
                teacher_data['gender'],
                teacher_data['address'],
                teacher_data['email'],
                teacher_data['mobilePhone'],
                teacher_data['homePhone'] if teacher_data['homePhone'] else None,
                teacher_data['specialization'],
                teacher_data['nic'],
                teacher_data['salary'],
                reg_no
            ))
            
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating teacher: {e}")
            return False
    
    def delete_teacher(self, reg_no):
        try:
            self.cursor.execute("DELETE FROM Teachers WHERE regNo=?", (reg_no,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting teacher: {e}")
            return False
    
    def get_all_teacher_reg_numbers(self):
        self.cursor.execute("SELECT regNo FROM Teachers ORDER BY regNo")
        return [str(row[0]) for row in self.cursor.fetchall()]
    
    def get_teacher_by_reg_no(self, reg_no):
        try:
            self.cursor.execute("""
            SELECT regNo, firstName, lastName, dateOfBirth, gender, address, 
                   email, mobilePhone, homePhone, specialization, nic, salary 
            FROM Teachers 
            WHERE regNo=?
            """, (reg_no,))
            
            row = self.cursor.fetchone()
            if row:
                return {
                    'regNo': row[0],
                    'firstName': row[1],
                    'lastName': row[2],
                    'dateOfBirth': row[3],
                    'gender': row[4],
                    'address': row[5],
                    'email': row[6],
                    'mobilePhone': row[7],
                    'homePhone': row[8],
                    'specialization': row[9],
                    'nic': row[10],
                    'salary': row[11]
                }
            return None
        except Exception as e:
            print(f"Error retrieving teacher: {e}")
            return None
    
    def get_teachers_count(self):
        self.cursor.execute("SELECT COUNT(*) FROM Teachers")
        return self.cursor.fetchone()[0]
    
    def search_teachers(self, search_term):
        try:
            query = """
            SELECT regNo, firstName, lastName, specialization FROM Teachers
            WHERE firstName LIKE ? OR lastName LIKE ? OR specialization LIKE ? OR nic LIKE ?
            ORDER BY firstName, lastName
            LIMIT 50
            """
            search_pattern = f"%{search_term}%"
            self.cursor.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error searching teachers: {e}")
            return []
    
    def close(self):
        if self.conn:
            self.conn.close()