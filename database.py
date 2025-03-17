# database.py
import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self):
        # Create database directory if it doesn't exist
        os.makedirs('database', exist_ok=True)
        self.conn = sqlite3.connect('database/student.db')
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        # Create registration table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Registration (
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
        
        # Create users table for login
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            username VARCHAR(50) PRIMARY KEY,
            password VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Insert default admin user if not exists
        self.cursor.execute("SELECT COUNT(*) FROM Users WHERE username = 'Admin'")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute("INSERT INTO Users (username, password) VALUES ('Admin', 'Skills@123')")
        
        self.conn.commit()
    
    def verify_login(self, username, password):
        """Verify user credentials for login"""
        self.cursor.execute("SELECT * FROM Users WHERE username=? AND password=?", 
                           (username, password))
        return self.cursor.fetchone() is not None
    
    def check_username_exists(self, username):
        """Check if a username already exists in the database"""
        self.cursor.execute("SELECT COUNT(*) FROM Users WHERE username=?", (username,))
        return self.cursor.fetchone()[0] > 0
    
    def create_user(self, username, password):
        """Create a new user account"""
        try:
            # Check if username already exists
            if self.check_username_exists(username):
                return False
            
            # Insert the new user
            self.cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", 
                              (username, password))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
    
    def insert_student(self, student_data):
        """Insert a new student record"""
        try:
            # Check if NIC already exists
            self.cursor.execute("SELECT COUNT(*) FROM Registration WHERE nic=?", 
                               (student_data['nic'],))
            if self.cursor.fetchone()[0] > 0:
                return False  # NIC already exists
            
            query = '''
            INSERT INTO Registration 
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
        """Update an existing student record"""
        try:
            query = '''
            UPDATE Registration 
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
        """Delete a student record"""
        try:
            self.cursor.execute("DELETE FROM Registration WHERE regNo=?", (reg_no,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting student: {e}")
            return False
    
    def get_all_reg_numbers(self):
        """Get all registration numbers for the dropdown"""
        self.cursor.execute("SELECT regNo FROM Registration ORDER BY regNo")
        return [str(row[0]) for row in self.cursor.fetchall()]
    
    def get_student_by_reg_no(self, reg_no):
        """Get student details by registration number"""
        try:
            self.cursor.execute("""
            SELECT regNo, firstName, lastName, dateOfBirth, gender, address, 
                   email, mobilePhone, homePhone, parentName, nic, contactNo 
            FROM Registration 
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
    
    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()