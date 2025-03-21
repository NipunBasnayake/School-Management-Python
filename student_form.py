import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import re

class StudentForm:
    def __init__(self, root, db, main_menu_window):
        self.root = root
        self.db = db
        self.main_menu_window = main_menu_window
        
        self.colors = {
            'primary': '#3498db',
            'secondary': '#2ecc71',
            'accent': '#f39c12',
            'danger': '#e74c3c',
            'background': '#f5f5f5',
            'card': '#ffffff',
            'text': '#2c3e50',
            'light_text': '#7f8c8d'
        }
        
        self.root.title("Student Management - EduPro Academy")
        self.root.configure(bg=self.colors['background'])
        
        window_width = 850
        window_height = 710 
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.setup_ui()
        self.load_reg_numbers()
    
    def setup_ui(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure('TEntry', 
                          background='white', 
                          foreground=self.colors['text'],
                          fieldbackground='white',
                          borderwidth=1)
        
        self.style.configure('TCombobox', 
                          background='white', 
                          foreground=self.colors['text'],
                          fieldbackground='white')
        
        self.style.configure('TButton', 
                          background=self.colors['primary'], 
                          foreground='white',
                          borderwidth=0,
                          focusthickness=3,
                          focuscolor=self.colors['primary'])
        
        self.style.map('TButton',
                    background=[('active', self.colors['secondary']), 
                                ('pressed', self.colors['secondary'])],
                    foreground=[('active', 'white'), 
                                ('pressed', 'white')])
        
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=80)  
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(header_frame, text="Student Management", 
                             font=("Helvetica", 20, "bold"),  
                             bg=self.colors['primary'], fg="white")
        header_label.pack(side=tk.LEFT, padx=30, pady=15)
        
        home_btn = tk.Label(header_frame, text="Home", font=("Helvetica", 12),
                         bg=self.colors['primary'], fg="white", cursor="hand2")
        home_btn.pack(side=tk.RIGHT, padx=(0, 20), pady=15)
        home_btn.bind("<Button-1>", lambda e: self.exit_form())
        
        logout_btn = tk.Label(header_frame, text="Logout", font=("Helvetica", 12),
                          bg=self.colors['primary'], fg="white", cursor="hand2")
        logout_btn.pack(side=tk.RIGHT, padx=(0, 15), pady=15)
        logout_btn.bind("<Button-1>", lambda e: self.logout())
        
        top_container = tk.Frame(self.root, bg=self.colors['background'], height=60)
        top_container.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        search_frame = tk.Frame(top_container, bg=self.colors['card'], bd=0)
        search_frame.pack(side=tk.LEFT, padx=(0, 10), fill=tk.Y)
        
        self.search_entry = ttk.Entry(search_frame, width=25, font=("Helvetica", 12), style='TEntry')
        self.search_entry.pack(side=tk.LEFT, padx=(15, 0), pady=10, ipady=7)
        
        search_btn = ttk.Button(search_frame, text="🔍 Search", style='TButton',
                           command=self.search_student)
        search_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        reg_frame = tk.Frame(top_container, bg=self.colors['card'], bd=0)
        reg_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        reg_label = tk.Label(reg_frame, text="Reg No:", bg=self.colors['card'], 
                          font=("Helvetica", 12), fg=self.colors['text'])
        reg_label.pack(side=tk.LEFT, padx=(15, 5), pady=10)
        
        self.reg_combo = ttk.Combobox(reg_frame, width=10, font=("Helvetica", 12), style='TCombobox')
        self.reg_combo.pack(side=tk.LEFT, padx=(0, 5), pady=10)
        
        load_btn = ttk.Button(reg_frame, text="Load", style='TButton',
                         command=lambda: self.load_student_data(None))
        load_btn.pack(side=tk.LEFT, padx=(0, 15), pady=10)
        
        add_new_btn = ttk.Button(top_container, text="+ Add New Student", style='TButton',
                             command=self.clear_fields)
        add_new_btn.pack(side=tk.RIGHT, padx=5, pady=10)
        
        main_frame = tk.Frame(self.root, bg=self.colors['background'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        left_frame = tk.Frame(main_frame, bg=self.colors['background'], width=400)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        
        right_frame = tk.Frame(main_frame, bg=self.colors['background'], width=400)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        
        basic_frame = tk.LabelFrame(left_frame, text="Basic Details", font=("Helvetica", 12, "bold"), 
                                  padx=15, pady=15, bg=self.colors['card'], fg=self.colors['primary'])
        basic_frame.pack(fill=tk.BOTH, pady=(0, 10))
        
        first_name_label = tk.Label(basic_frame, text="First Name", bg=self.colors['card'], 
                                 font=("Helvetica", 11), fg=self.colors['text'])
        first_name_label.grid(row=0, column=0, padx=10, pady=8, sticky=tk.W)
        
        self.first_name_entry = ttk.Entry(basic_frame, width=25, font=("Helvetica", 11), style='TEntry')
        self.first_name_entry.grid(row=0, column=1, padx=10, pady=8, sticky=tk.W)
        
        last_name_label = tk.Label(basic_frame, text="Last Name", bg=self.colors['card'], 
                                font=("Helvetica", 11), fg=self.colors['text'])
        last_name_label.grid(row=1, column=0, padx=10, pady=8, sticky=tk.W)
        
        self.last_name_entry = ttk.Entry(basic_frame, width=25, font=("Helvetica", 11), style='TEntry')
        self.last_name_entry.grid(row=1, column=1, padx=10, pady=8, sticky=tk.W)
        
        dob_label = tk.Label(basic_frame, text="Date of Birth", bg=self.colors['card'], 
                          font=("Helvetica", 11), fg=self.colors['text'])
        dob_label.grid(row=2, column=0, padx=10, pady=8, sticky=tk.W)
        
        self.dob_entry = DateEntry(basic_frame, width=23, background=self.colors['primary'],
                                foreground='white', borderwidth=0, font=("Helvetica", 11),
                                date_pattern='yyyy-mm-dd')
        self.dob_entry.grid(row=2, column=1, padx=10, pady=8, sticky=tk.W)
        
        gender_label = tk.Label(basic_frame, text="Gender", bg=self.colors['card'], 
                             font=("Helvetica", 11), fg=self.colors['text'])
        gender_label.grid(row=3, column=0, padx=10, pady=8, sticky=tk.W)
        
        gender_frame = tk.Frame(basic_frame, bg=self.colors['card'])
        gender_frame.grid(row=3, column=1, padx=10, pady=8, sticky=tk.W)
        
        self.gender_var = tk.StringVar()
        
        male_radio = tk.Radiobutton(gender_frame, text="Male", variable=self.gender_var, value="Male", 
                                 bg=self.colors['card'], font=("Helvetica", 11), fg=self.colors['text'],
                                 activebackground=self.colors['card'])
        male_radio.pack(side=tk.LEFT, padx=(0, 15))
        
        female_radio = tk.Radiobutton(gender_frame, text="Female", variable=self.gender_var, value="Female", 
                                   bg=self.colors['card'], font=("Helvetica", 11), fg=self.colors['text'],
                                   activebackground=self.colors['card'])
        female_radio.pack(side=tk.LEFT)
        
        contact_frame = tk.LabelFrame(left_frame, text="Contact Details", font=("Helvetica", 12, "bold"), 
                                    padx=15, pady=15, bg=self.colors['card'], fg=self.colors['secondary'])
        contact_frame.pack(fill=tk.BOTH, expand=True)
        
        address_label = tk.Label(contact_frame, text="Address", bg=self.colors['card'], 
                              font=("Helvetica", 11), fg=self.colors['text'])
        address_label.grid(row=0, column=0, padx=10, pady=8, sticky=tk.NW)
        
        self.address_text = tk.Text(contact_frame, width=25, height=3, font=("Helvetica", 11),
                                 bd=1, relief=tk.SOLID)
        self.address_text.grid(row=0, column=1, padx=10, pady=8, sticky=tk.W)
        
        email_label = tk.Label(contact_frame, text="Email", bg=self.colors['card'], 
                            font=("Helvetica", 11), fg=self.colors['text'])
        email_label.grid(row=1, column=0, padx=10, pady=8, sticky=tk.W)
        
        self.email_entry = ttk.Entry(contact_frame, width=25, font=("Helvetica", 11), style='TEntry')
        self.email_entry.grid(row=1, column=1, padx=10, pady=8, sticky=tk.W)
        
        mobile_label = tk.Label(contact_frame, text="Mobile Phone", bg=self.colors['card'], 
                             font=("Helvetica", 11), fg=self.colors['text'])
        mobile_label.grid(row=2, column=0, padx=10, pady=8, sticky=tk.W)
        
        self.mobile_entry = ttk.Entry(contact_frame, width=25, font=("Helvetica", 11), style='TEntry')
        self.mobile_entry.grid(row=2, column=1, padx=10, pady=8, sticky=tk.W)
        
        home_label = tk.Label(contact_frame, text="Home Phone", bg=self.colors['card'], 
                           font=("Helvetica", 11), fg=self.colors['text'])
        home_label.grid(row=3, column=0, padx=10, pady=8, sticky=tk.W)
        
        self.home_entry = ttk.Entry(contact_frame, width=25, font=("Helvetica", 11), style='TEntry')
        self.home_entry.grid(row=3, column=1, padx=10, pady=8, sticky=tk.W)
        
        parent_frame = tk.LabelFrame(right_frame, text="Parent/Guardian Details", font=("Helvetica", 12, "bold"), 
                                   padx=15, pady=15, bg=self.colors['card'], fg=self.colors['accent'])
        parent_frame.pack(fill=tk.BOTH, pady=(0, 10))
        
        parent_name_label = tk.Label(parent_frame, text="Parent Name", bg=self.colors['card'], 
                                  font=("Helvetica", 11), fg=self.colors['text'])
        parent_name_label.grid(row=0, column=0, padx=10, pady=8, sticky=tk.W)
        
        self.parent_name_entry = ttk.Entry(parent_frame, width=25, font=("Helvetica", 11), style='TEntry')
        self.parent_name_entry.grid(row=0, column=1, padx=10, pady=8, sticky=tk.W)
        
        nic_label = tk.Label(parent_frame, text="NIC", bg=self.colors['card'], 
                          font=("Helvetica", 11), fg=self.colors['text'])
        nic_label.grid(row=1, column=0, padx=10, pady=8, sticky=tk.W)
        
        self.nic_entry = ttk.Entry(parent_frame, width=25, font=("Helvetica", 11), style='TEntry')
        self.nic_entry.grid(row=1, column=1, padx=10, pady=8, sticky=tk.W)
        
        contact_label = tk.Label(parent_frame, text="Contact No", bg=self.colors['card'], 
                              font=("Helvetica", 11), fg=self.colors['text'])
        contact_label.grid(row=2, column=0, padx=10, pady=8, sticky=tk.W)
        
        self.contact_entry = ttk.Entry(parent_frame, width=25, font=("Helvetica", 11), style='TEntry')
        self.contact_entry.grid(row=2, column=1, padx=10, pady=8, sticky=tk.W)
        
        additional_frame = tk.LabelFrame(right_frame, text="Additional Information", font=("Helvetica", 12, "bold"), 
                                      padx=15, pady=15, bg=self.colors['card'], fg=self.colors['primary'])
        additional_frame.pack(fill=tk.BOTH, expand=True)
        
        preview_label = tk.Label(additional_frame, text="Student Preview", bg=self.colors['card'], 
                              font=("Helvetica", 11, "bold"), fg=self.colors['text'])
        preview_label.pack(anchor=tk.W, padx=10, pady=(0, 5))
        
        self.preview_text = tk.Text(additional_frame, width=40, height=9, font=("Helvetica", 10),
                                 bd=1, relief=tk.SOLID, state=tk.DISABLED)
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        button_frame = tk.Frame(self.root, bg=self.colors['background'], height=70)
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        register_button = ttk.Button(button_frame, text="Register", width=15, 
                                command=self.register_student, style='TButton')
        register_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        update_button = ttk.Button(button_frame, text="Update", width=15, 
                              command=self.update_student, style='TButton')
        update_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        clear_button = ttk.Button(button_frame, text="Clear", width=15, 
                             command=self.clear_fields)
        clear_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.style.configure('Danger.TButton', 
                          background=self.colors['danger'], 
                          foreground='white')
        
        self.style.map('Danger.TButton',
                    background=[('active', '#c0392b'), 
                                ('pressed', '#c0392b')],
                    foreground=[('active', 'white'), 
                                ('pressed', 'white')])
        
        delete_button = ttk.Button(button_frame, text="Delete", width=15, 
                              command=self.delete_student, style='Danger.TButton')
        delete_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        back_button = ttk.Button(button_frame, text="Back to Home", width=15, 
                            command=self.exit_form)
        back_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        self.root.protocol("WM_DELETE_WINDOW", self.exit_form)
        
        self.search_entry.bind("<Return>", lambda e: self.search_student())
        
        self.first_name_entry.bind("<KeyRelease>", lambda e: self.update_preview())
        self.last_name_entry.bind("<KeyRelease>", lambda e: self.update_preview())
        self.dob_entry.bind("<<DateEntrySelected>>", lambda e: self.update_preview())
        self.email_entry.bind("<KeyRelease>", lambda e: self.update_preview())
        self.mobile_entry.bind("<KeyRelease>", lambda e: self.update_preview())
        
        self.reg_combo.bind("<<ComboboxSelected>>", self.load_student_data)
    
    def load_reg_numbers(self):
        reg_numbers = self.db.get_all_student_reg_numbers()
        self.reg_combo['values'] = reg_numbers
        if not reg_numbers:
            self.reg_combo.set("")
    
    def load_student_data(self, event):
        reg_no = self.reg_combo.get()
        if reg_no:
            student = self.db.get_student_by_reg_no(reg_no)
            if student:
                self.fill_form_with_student_data(student)
                self.update_preview()
            else:
                messagebox.showinfo("Information", f"No student found with registration number {reg_no}")
    
    def fill_form_with_student_data(self, student):
        self.first_name_entry.delete(0, tk.END)
        self.first_name_entry.insert(0, student['firstName'])
        
        self.last_name_entry.delete(0, tk.END)
        self.last_name_entry.insert(0, student['lastName'])
        
        try:
            date_obj = datetime.strptime(student['dateOfBirth'], '%Y-%m-%d')
            self.dob_entry.set_date(date_obj)
        except:
            self.dob_entry.set_date(datetime.now())
        
        self.gender_var.set(student['gender'])
        
        self.address_text.delete(1.0, tk.END)
        self.address_text.insert(tk.END, student['address'])
        
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, student['email'])
        
        self.mobile_entry.delete(0, tk.END)
        self.mobile_entry.insert(0, str(student['mobilePhone']))
        
        self.home_entry.delete(0, tk.END)
        if student['homePhone']:
            self.home_entry.insert(0, str(student['homePhone']))
        
        self.parent_name_entry.delete(0, tk.END)
        self.parent_name_entry.insert(0, student['parentName'])
        
        self.nic_entry.delete(0, tk.END)
        self.nic_entry.insert(0, student['nic'])
        
        self.contact_entry.delete(0, tk.END)
        self.contact_entry.insert(0, str(student['contactNo']))
    
    def get_form_data(self):
        return {
            'firstName': self.first_name_entry.get(),
            'lastName': self.last_name_entry.get(),
            'dateOfBirth': self.dob_entry.get_date().strftime('%Y-%m-%d'),
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
        
        if not self.validate_data(student_data):
            return
        
        result = self.db.insert_student(student_data)
        
        if result:
            messagebox.showinfo("Success", "Student registered successfully!")
            self.clear_fields()
            self.load_reg_numbers()
        else:
            messagebox.showerror("Error", "Failed to register student. NIC may already exist.")
    
    def update_student(self):
        reg_no = self.reg_combo.get()
        if not reg_no:
            messagebox.showerror("Error", "Please select a registration number.")
            return
        
        student_data = self.get_form_data()
        
        if not self.validate_data(student_data):
            return
        
        result = self.db.update_student(reg_no, student_data)
        
        if result:
            messagebox.showinfo("Success", "Student information updated successfully!")
            self.load_reg_numbers()
            self.update_preview()
        else:
            messagebox.showerror("Error", "Failed to update student information. NIC may already exist.")
    
    def delete_student(self):
        reg_no = self.reg_combo.get()
        if not reg_no:
            messagebox.showerror("Error", "Please select a registration number.")
            return
        
        if messagebox.askyesno("Confirm Delete", 
                             "Are you sure you want to delete this student record? This action cannot be undone.",
                             icon='warning'):
            result = self.db.delete_student(reg_no)
            
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
        self.dob_entry.set_date(datetime.now())
        self.gender_var.set("")
        self.address_text.delete(1.0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.mobile_entry.delete(0, tk.END)
        self.home_entry.delete(0, tk.END)
        self.parent_name_entry.delete(0, tk.END)
        self.nic_entry.delete(0, tk.END)
        self.contact_entry.delete(0, tk.END)
        
        self.update_preview()
        
        self.first_name_entry.focus()
    
    def validate_data(self, data):
        if not data['firstName'] or not data['lastName']:
            messagebox.showerror("Validation Error", "First Name and Last Name are required.")
            return False
        
        if not data['gender']:
            messagebox.showerror("Validation Error", "Please select a gender.")
            return False
        
        if not data['address']:
            messagebox.showerror("Validation Error", "Address is required.")
            return False
        
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not data['email'] or not re.match(email_pattern, data['email']):
            messagebox.showerror("Validation Error", "Please enter a valid email address.")
            return False
        
        if not data['nic']:
            messagebox.showerror("Validation Error", "NIC is required.")
            return False
        
        if not data['parentName']:
            messagebox.showerror("Validation Error", "Parent Name is required.")
            return False
        
        try:
            if not data['mobilePhone']:
                messagebox.showerror("Validation Error", "Mobile Phone is required.")
                return False
            int(data['mobilePhone'])
            
            if data['homePhone']:
                int(data['homePhone'])
            
            if not data['contactNo']:
                messagebox.showerror("Validation Error", "Contact Number is required.")
                return False
            int(data['contactNo'])
        except ValueError:
            messagebox.showerror("Validation Error", "Phone numbers must be numeric values.")
            return False
        
        dob = datetime.strptime(data['dateOfBirth'], '%Y-%m-%d')
        today = datetime.now()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        
        if age < 5:
            messagebox.showwarning("Validation Warning", 
                               "Student appears to be younger than 5 years old. Please verify the date of birth.")
            
        return True
    
    def update_preview(self):
        self.preview_text.config(state=tk.NORMAL)
        self.preview_text.delete(1.0, tk.END)
        
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        
        if not first_name and not last_name:
            self.preview_text.insert(tk.END, "Enter student details to see a preview.")
            self.preview_text.config(state=tk.DISABLED)
            return
        
        preview = f"Name: {first_name} {last_name}\n"
        
        if self.gender_var.get():
            preview += f"Gender: {self.gender_var.get()}\n"
        
        dob = self.dob_entry.get_date().strftime('%Y-%m-%d')
        if dob:
            preview += f"Date of Birth: {dob}\n"
        
        email = self.email_entry.get()
        if email:
            preview += f"Email: {email}\n"
        
        mobile = self.mobile_entry.get()
        if mobile:
            preview += f"Mobile: {mobile}\n"
        
        reg_no = self.reg_combo.get()
        if reg_no:
            preview += f"Registration No: {reg_no}\n"
        
        if self.nic_entry.get():
            preview += f"NIC: {self.nic_entry.get()}\n"
        
        parent_name = self.parent_name_entry.get()
        if parent_name:
            preview += f"Parent: {parent_name}\n"
        
        self.preview_text.insert(tk.END, preview)
        self.preview_text.config(state=tk.DISABLED)
    
    def search_student(self):
        search_term = self.search_entry.get().strip()
        if not search_term:
            messagebox.showinfo("Search", "Please enter a search term.")
            return
        
        results = self.db.search_students(search_term)
        
        if not results:
            messagebox.showinfo("Search Results", "No matching students found.")
            return
        
        self.show_search_results(results)
    
    def show_search_results(self, results):
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Results - Students")
        search_window.configure(bg=self.colors['background'])
        search_window.grab_set()
        
        window_width = 500
        window_height = 400
        screen_width = search_window.winfo_screenwidth()
        screen_height = search_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        search_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        header_frame = tk.Frame(search_window, bg=self.colors['primary'], height=60)
        header_frame.pack(fill=tk.X)
        
        label = tk.Label(header_frame, text="Search Results", 
                      font=("Helvetica", 16, "bold"), 
                      bg=self.colors['primary'], fg="white")
        label.place(relx=0.5, rely=0.5, anchor="center")
        
        result_frame = tk.Frame(search_window, bg=self.colors['card'], bd=0)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(15, 20))
        
        columns = ("Reg No", "First Name", "Last Name")
        tree = ttk.Treeview(result_frame, columns=columns, show="headings", height=10)
        
        self.style.configure("Treeview", 
                          background=self.colors['card'],
                          foreground=self.colors['text'],
                          rowheight=30,
                          fieldbackground=self.colors['card'])
        
        self.style.configure("Treeview.Heading",
                          background=self.colors['primary'],
                          foreground="white",
                          relief="flat")
        
        self.style.map("Treeview.Heading",
                    background=[('active', self.colors['primary_dark'])])
        
        tree.heading("Reg No", text="Reg No")
        tree.heading("First Name", text="First Name")
        tree.heading("Last Name", text="Last Name")
        
        tree.column("Reg No", width=80)
        tree.column("First Name", width=150)
        tree.column("Last Name", width=150)
        
        for row in results:
            tree.insert("", "end", values=row)
        
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        def select_item():
            selected = tree.selection()
            if selected:
                item = tree.item(selected[0])
                reg_no = item['values'][0]
                self.reg_combo.set(str(reg_no))
                self.load_student_data(None)
                search_window.destroy()
        
        button_frame = tk.Frame(search_window, bg=self.colors['background'])
        button_frame.pack(fill=tk.X, pady=(0, 15))
        
        select_btn = ttk.Button(button_frame, text="Select Student", style='TButton',
                             command=select_item)
        select_btn.pack(side=tk.LEFT, padx=(20, 10))
        
        cancel_btn = ttk.Button(button_frame, text="Cancel", 
                             command=search_window.destroy)
        cancel_btn.pack(side=tk.LEFT)
        
        tree.bind("<Double-1>", lambda e: select_item())
    
    def logout(self):
        if messagebox.askyesno("Confirm Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            self.main_menu_window.destroy()
            for widget in self.root.master.winfo_children():
                if isinstance(widget, tk.Toplevel) and hasattr(widget, 'title') and 'Login' in widget.title():
                    widget.deiconify()
    
    def exit_form(self):
        self.root.destroy()
        self.main_menu_window.deiconify()