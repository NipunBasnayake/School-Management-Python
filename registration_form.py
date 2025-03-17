# registration_form.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class RegistrationForm:
    def __init__(self, root, db, login_window):
        self.root = root
        self.db = db
        self.login_window = login_window
        
        self.root.title("Skills International - Student Registration")
        self.root.geometry("750x650")
        self.setup_ui()
        self.load_reg_numbers()
    
    def setup_ui(self):
        # Main title
        title_label = tk.Label(self.root, text="Skills International", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)
        
        # Logout and Exit links at the top right
        links_frame = tk.Frame(self.root)
        links_frame.pack(anchor="ne", padx=20)
        
        logout_link = tk.Label(links_frame, text="Logout", fg="blue", cursor="hand2")
        logout_link.pack(side=tk.LEFT, padx=10)
        logout_link.bind("<Button-1>", self.logout)
        
        exit_link = tk.Label(links_frame, text="Exit", fg="blue", cursor="hand2")
        exit_link.pack(side=tk.LEFT)
        exit_link.bind("<Button-1>", self.exit_app)
        
        # Main container frame
        main_frame = tk.Frame(self.root, bd=2, relief=tk.GROOVE)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 1. Student Registration Group
        reg_frame = tk.LabelFrame(main_frame, text="Student Registration")
        reg_frame.pack(fill=tk.X, padx=20, pady=10)
        
        reg_label = tk.Label(reg_frame, text="Reg No")
        reg_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        
        self.reg_combo = ttk.Combobox(reg_frame, width=20)
        self.reg_combo.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
        self.reg_combo.bind("<<ComboboxSelected>>", self.load_student_data)
        
        # 2. Basic Details Group
        basic_frame = tk.LabelFrame(main_frame, text="Basic Details")
        basic_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # First Name
        first_name_label = tk.Label(basic_frame, text="First Name")
        first_name_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.first_name_entry = tk.Entry(basic_frame, width=30)
        self.first_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        
        # Last Name
        last_name_label = tk.Label(basic_frame, text="Last Name")
        last_name_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.last_name_entry = tk.Entry(basic_frame, width=30)
        self.last_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
        
        # Date of Birth
        dob_label = tk.Label(basic_frame, text="Date of Birth")
        dob_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        
        # Date picker (simplified version)
        dob_frame = tk.Frame(basic_frame)
        dob_frame.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)
        
        # For a proper date picker, you might want to use tkcalendar library
        self.dob_entry = tk.Entry(dob_frame, width=30)
        self.dob_entry.pack(side=tk.LEFT)
        self.dob_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Gender
        gender_label = tk.Label(basic_frame, text="Gender")
        gender_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        
        gender_frame = tk.Frame(basic_frame)
        gender_frame.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)
        
        self.gender_var = tk.StringVar()
        self.gender_var.set("")
        
        male_radio = tk.Radiobutton(gender_frame, text="Male", variable=self.gender_var, value="Male")
        male_radio.pack(side=tk.LEFT, padx=5)
        
        female_radio = tk.Radiobutton(gender_frame, text="Female", variable=self.gender_var, value="Female")
        female_radio.pack(side=tk.LEFT, padx=5)
        
        # 3. Contact Details Group
        contact_frame = tk.LabelFrame(main_frame, text="Contact Details")
        contact_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Address
        address_label = tk.Label(contact_frame, text="Address")
        address_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.address_text = tk.Text(contact_frame, width=30, height=3)
        self.address_text.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        
        # Email
        email_label = tk.Label(contact_frame, text="Email")
        email_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.email_entry = tk.Entry(contact_frame, width=30)
        self.email_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
        
        # Mobile Phone
        mobile_label = tk.Label(contact_frame, text="Mobile Phone")
        mobile_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.mobile_entry = tk.Entry(contact_frame, width=30)
        self.mobile_entry.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)
        
        # Home Phone
        home_label = tk.Label(contact_frame, text="Home Phone")
        home_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.home_entry = tk.Entry(contact_frame, width=30)
        self.home_entry.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)
        
        # 4. Parent Details Group
        parent_frame = tk.LabelFrame(main_frame, text="Parent Details")
        parent_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Parent Name
        parent_name_label = tk.Label(parent_frame, text="Parent Name")
        parent_name_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.parent_name_entry = tk.Entry(parent_frame, width=30)
        self.parent_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        
        # NIC
        nic_label = tk.Label(parent_frame, text="NIC")
        nic_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.nic_entry = tk.Entry(parent_frame, width=30)
        self.nic_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
        
        # Contact No
        contact_label = tk.Label(parent_frame, text="Contact No")
        contact_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.contact_entry = tk.Entry(parent_frame, width=30)
        self.contact_entry.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)
        
        # 5. Button Group
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        register_button = tk.Button(button_frame, text="Register", width=10, command=self.register_student)
        register_button.grid(row=0, column=0, padx=10)
        
        update_button = tk.Button(button_frame, text="Update", width=10, command=self.update_student)
        update_button.grid(row=0, column=1, padx=10)
        
        clear_button = tk.Button(button_frame, text="Clear", width=10, command=self.clear_fields)
        clear_button.grid(row=0, column=2, padx=10)
        
        delete_button = tk.Button(button_frame, text="Delete", width=10, command=self.delete_student)
        delete_button.grid(row=0, column=3, padx=10)
    
    # Methods for functionality
    def load_reg_numbers(self):
        # Get all registration numbers from the database
        self.reg_combo['values'] = self.db.get_all_reg_numbers()  # You need to implement this in the Database class
    
    def load_student_data(self, event):
        reg_no = self.reg_combo.get()
        if reg_no:
            # Get student data from the database
            student = self.db.get_student_by_reg_no(reg_no)  # Implement this method
            if student:
                # Fill the form with the student data
                self.fill_form_with_student_data(student)
    
    def fill_form_with_student_data(self, student):
        # Example implementation - adjust based on your database structure
        self.first_name_entry.delete(0, tk.END)
        self.first_name_entry.insert(0, student['firstName'])
        
        self.last_name_entry.delete(0, tk.END)
        self.last_name_entry.insert(0, student['lastName'])
        
        self.dob_entry.delete(0, tk.END)
        self.dob_entry.insert(0, student['dateOfBirth'])
        
        self.gender_var.set(student['gender'])
        
        self.address_text.delete(1.0, tk.END)
        self.address_text.insert(tk.END, student['address'])
        
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, student['email'])
        
        self.mobile_entry.delete(0, tk.END)
        self.mobile_entry.insert(0, str(student['mobilePhone']))
        
        self.home_entry.delete(0, tk.END)
        self.home_entry.insert(0, str(student['homePhone']))
        
        self.parent_name_entry.delete(0, tk.END)
        self.parent_name_entry.insert(0, student['parentName'])
        
        self.nic_entry.delete(0, tk.END)
        self.nic_entry.insert(0, student['nic'])
        
        self.contact_entry.delete(0, tk.END)
        self.contact_entry.insert(0, str(student['contactNo']))
    
    def get_form_data(self):
        # Get all data from the form
        return {
            'firstName': self.first_name_entry.get(),
            'lastName': self.last_name_entry.get(),
            'dateOfBirth': self.dob_entry.get(),
            'gender': self.gender_var.get(),
            'address': self.address_text.get(1.0, tk.END).strip(),
            'email': self.email_entry.get(),
            'mobilePhone': self.mobile_entry.get(),
            'homePhone': self.home_entry.get(),
            'parentName': self.parent_name_entry.get(),
            'nic': self.nic_entry.get(),
            'contactNo': self.contact_entry.get()
        }
    
    def register_student(self):
        student_data = self.get_form_data()
        
        # Validate the data
        if not self.validate_data(student_data):
            return
        
        # Insert the data into the database
        result = self.db.insert_student(student_data)  # Implement this method
        
        if result:
            messagebox.showinfo("Success", "Student registered successfully!")
            self.clear_fields()
            self.load_reg_numbers()  # Refresh the registration numbers
        else:
            messagebox.showerror("Error", "Failed to register student.")
    
    def update_student(self):
        reg_no = self.reg_combo.get()
        if not reg_no:
            messagebox.showerror("Error", "Please select a registration number.")
            return
        
        student_data = self.get_form_data()
        
        # Validate the data
        if not self.validate_data(student_data):
            return
        
        # Update the data in the database
        result = self.db.update_student(reg_no, student_data)  # Implement this method
        
        if result:
            messagebox.showinfo("Success", "Student information updated successfully!")
            self.load_reg_numbers()
        else:
            messagebox.showerror("Error", "Failed to update student information.")
    
    def delete_student(self):
        reg_no = self.reg_combo.get()
        if not reg_no:
            messagebox.showerror("Error", "Please select a registration number.")
            return
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this student record?"):
            # Delete the student from the database
            result = self.db.delete_student(reg_no)  # Implement this method
            
            if result:
                messagebox.showinfo("Success", "Student record deleted successfully!")
                self.clear_fields()
                self.load_reg_numbers()
            else:
                messagebox.showerror("Error", "Failed to delete student record.")
    
    def clear_fields(self):
        self.reg_combo.set('')
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.dob_entry.delete(0, tk.END)
        self.dob_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.gender_var.set("")
        self.address_text.delete(1.0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.mobile_entry.delete(0, tk.END)
        self.home_entry.delete(0, tk.END)
        self.parent_name_entry.delete(0, tk.END)
        self.nic_entry.delete(0, tk.END)
        self.contact_entry.delete(0, tk.END)
    
    def validate_data(self, data):
        # Basic validation
        if not data['firstName'] or not data['lastName']:
            messagebox.showerror("Error", "First Name and Last Name are required.")
            return False
        
        if not data['gender']:
            messagebox.showerror("Error", "Please select a gender.")
            return False
        
        if not data['email'] or '@' not in data['email']:
            messagebox.showerror("Error", "Please enter a valid email address.")
            return False
        
        try:
            # Check if mobile phone is a number
            if data['mobilePhone']:
                int(data['mobilePhone'])
            
            # Check if home phone is a number
            if data['homePhone']:
                int(data['homePhone'])
            
            # Check if contact number is a number
            if data['contactNo']:
                int(data['contactNo'])
        except ValueError:
            messagebox.showerror("Error", "Phone numbers must be numeric values.")
            return False
        
        return True
    
    def logout(self, event=None):
        if messagebox.askyesno("Confirm Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            self.login_window.deiconify()  # Show login window again
    
    def exit_app(self, event=None):
        if messagebox.askyesno("Exit Application", "Are you sure you want to exit?"):
            self.root.destroy()
            self.login_window.destroy()  # Close login window as well