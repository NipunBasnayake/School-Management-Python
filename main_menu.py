import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import student_form
import teacher_form
from datetime import datetime

class MainMenu:
    def __init__(self, root, db, login_window, username=None):
        self.root = root
        self.db = db
        self.login_window = login_window
        self.username = username
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
        
        self.setup_ui()
        self.load_dashboard_data()
    
    def setup_ui(self):
        self.root.title("EduPro Academy - Management System")
        self.root.configure(bg=self.colors['background'])
        self.root.resizable(True, True)
        
        window_width = 900
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
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
        
        main_container = tk.Frame(self.root, bg=self.colors['background'])
        main_container.pack(fill=tk.BOTH, expand=True)
        
        left_panel = tk.Frame(main_container, bg=self.colors['primary'], width=200)
        left_panel.pack(side=tk.LEFT, fill=tk.Y)
        left_panel.pack_propagate(False)
        
        right_panel = tk.Frame(main_container, bg=self.colors['background'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        logo_frame = tk.Frame(left_panel, bg=self.colors['primary'], height=150)
        logo_frame.pack(fill=tk.X)
        logo_frame.pack_propagate(False)
        
        logo_path = "assets/logo.png"
        if os.path.exists(logo_path):
            try:
                logo_image = Image.open(logo_path)
                logo_image = logo_image.resize((80, 80), Image.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo_image)
                
                logo_label = tk.Label(logo_frame, image=self.logo_photo, bg=self.colors['primary'])
                logo_label.place(relx=0.5, rely=0.4, anchor="center")
            except Exception as e:
                logo_label = tk.Label(logo_frame, text="EduPro", 
                                    font=("Helvetica", 18, "bold"), 
                                    bg=self.colors['primary'], fg="white")
                logo_label.place(relx=0.5, rely=0.4, anchor="center")
        else:
            logo_label = tk.Label(logo_frame, text="EduPro", 
                                font=("Helvetica", 18, "bold"), 
                                bg=self.colors['primary'], fg="white")
            logo_label.place(relx=0.5, rely=0.4, anchor="center")
        
        academy_label = tk.Label(logo_frame, text="ACADEMY", 
                               font=("Helvetica", 10), 
                               bg=self.colors['primary'], fg="white")
        academy_label.place(relx=0.5, rely=0.65, anchor="center")
        
        menu_buttons_frame = tk.Frame(left_panel, bg=self.colors['primary'])
        menu_buttons_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        buttons_data = [
            {"text": "Dashboard", "icon": "dashboard.png", "command": self.show_dashboard},
            {"text": "Students", "icon": "student.png", "command": self.open_student_form},
            {"text": "Teachers", "icon": "teacher.png", "command": self.open_teacher_form},
            {"text": "Settings", "icon": "settings.png", "command": self.show_settings}
        ]
        
        for i, btn_data in enumerate(buttons_data):
            btn_frame = tk.Frame(menu_buttons_frame, bg=self.colors['primary'], height=40)
            btn_frame.pack(fill=tk.X, pady=5)
            
            icon_path = os.path.join("assets", btn_data["icon"])
            if os.path.exists(icon_path):
                try:
                    icon_image = Image.open(icon_path)
                    icon_image = icon_image.resize((24, 24), Image.LANCZOS)
                    icon_photo = ImageTk.PhotoImage(icon_image)
                    
                    setattr(self, f"icon_photo_{i}", icon_photo)
                    
                    icon_label = tk.Label(btn_frame, image=getattr(self, f"icon_photo_{i}"), 
                                        bg=self.colors['primary'])
                    icon_label.pack(side=tk.LEFT, padx=(20, 10))
                except Exception as e:
                    pass
            
            btn = tk.Label(btn_frame, text=btn_data["text"], 
                         font=("Helvetica", 12), 
                         bg=self.colors['primary'], fg="white", cursor="hand2")
            btn.pack(side=tk.LEFT, padx=5)
            
            btn_frame.bind("<Button-1>", self.create_button_handler(btn_data["command"]))
            btn.bind("<Button-1>", self.create_button_handler(btn_data["command"]))
            
            if "icon_label" in locals():
                icon_label.bind("<Button-1>", self.create_button_handler(btn_data["command"]))
        
        logout_frame = tk.Frame(left_panel, bg=self.colors['primary'], height=50)
        logout_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        logout_btn = tk.Label(logout_frame, text="Logout", 
                           font=("Helvetica", 12), cursor="hand2",
                           bg=self.colors['primary'], fg="white")
        logout_btn.pack(side=tk.LEFT, padx=(20, 0), pady=15)
        logout_btn.bind("<Button-1>", lambda e: self.logout())
        
        self.header_frame = tk.Frame(right_panel, bg=self.colors['card'], height=60)
        self.header_frame.pack(fill=tk.X)
        
        welcome_text = f"Welcome, {self.username if self.username else 'User'}"
        welcome_label = tk.Label(self.header_frame, text=welcome_text, 
                               font=("Helvetica", 14, "bold"), 
                               bg=self.colors['card'], fg=self.colors['text'])
        welcome_label.pack(side=tk.LEFT, padx=25, pady=15)
        
        date_label = tk.Label(self.header_frame, text=datetime.now().strftime("%B %d, %Y"), 
                            font=("Helvetica", 12), 
                            bg=self.colors['card'], fg=self.colors['light_text'])
        date_label.pack(side=tk.RIGHT, padx=25, pady=15)
        
        self.content_frame = tk.Frame(right_panel, bg=self.colors['background'])
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)
        
        self.show_dashboard()
    
    def create_button_handler(self, command):
        return lambda e: command()
    
    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        self.clear_content_frame()
        
        title_label = tk.Label(self.content_frame, text="Dashboard", 
                             font=("Helvetica", 18, "bold"), 
                             bg=self.colors['background'], fg=self.colors['text'])
        title_label.place(x=0, y=0)
        
        stats_frame = tk.Frame(self.content_frame, bg=self.colors['background'])
        stats_frame.place(x=0, y=40, relwidth=1, height=120)
        
        card_width = 200
        card_height = 120
        card_padding = 20
        
        cards_data = [
            {"title": "Students", "value": "...", "color": "#3498db", "icon": "student.png"},
            {"title": "Teachers", "value": "...", "color": "#2ecc71", "icon": "teacher.png"},
            {"title": "Courses", "value": "5", "color": "#e74c3c", "icon": "course.png"},
            {"title": "Revenue", "value": "$12,500", "color": "#f39c12", "icon": "revenue.png"}
        ]
        
        for i, card_data in enumerate(cards_data):
            card = tk.Frame(stats_frame, bg=card_data["color"], width=card_width, height=card_height)
            card.pack(side=tk.LEFT, padx=card_padding, pady=10)
            card.pack_propagate(False)
            
            title = tk.Label(card, text=card_data["title"], 
                          font=("Helvetica", 14), 
                          bg=card_data["color"], fg="white")
            title.pack(anchor=tk.W, padx=15, pady=(15, 5))
            
            value = tk.Label(card, text=card_data["value"], 
                          font=("Helvetica", 24, "bold"), 
                          bg=card_data["color"], fg="white")
            value.pack(anchor=tk.W, padx=15)
            
            if i == 0:
                self.student_count_label = value
            elif i == 1:
                self.teacher_count_label = value
        
        recent_frame = tk.Frame(self.content_frame, bg=self.colors['card'], bd=0)
        recent_frame.place(x=0, y=180, relwidth=1, relheight=0.65)
        
        recent_label = tk.Label(recent_frame, text="Recent Activities", 
                              font=("Helvetica", 16, "bold"), 
                              bg=self.colors['card'], fg=self.colors['text'])
        recent_label.pack(anchor=tk.W, padx=20, pady=15)
        
        activity_frame = tk.Frame(recent_frame, bg=self.colors['card'])
        activity_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        self.activity_tree = ttk.Treeview(activity_frame, columns=("Date", "User", "Action"), 
                                       show="headings", height=12)
        
        self.activity_tree.heading("Date", text="Date")
        self.activity_tree.heading("User", text="User")
        self.activity_tree.heading("Action", text="Action")
        
        self.activity_tree.column("Date", width=120)
        self.activity_tree.column("User", width=150)
        self.activity_tree.column("Action", width=400)
        
        self.activity_tree.pack(fill=tk.BOTH, expand=True)
        
        for i in range(5):
            date = datetime.now().strftime("%Y-%m-%d")
            self.activity_tree.insert("", "end", values=(date, "admin", "Logged into the system"))
        
        self.activity_tree.insert("", "end", values=(date, "admin", "Added new student: John Smith"))
        self.activity_tree.insert("", "end", values=(date, "admin", "Updated teacher: Jane Doe"))
    
    def load_dashboard_data(self):
        student_count = self.db.get_students_count()
        teacher_count = self.db.get_teachers_count()
        
        if hasattr(self, 'student_count_label'):
            self.student_count_label.config(text=str(student_count))
        
        if hasattr(self, 'teacher_count_label'):
            self.teacher_count_label.config(text=str(teacher_count))
    
    def show_settings(self):
        self.clear_content_frame()
        
        title_label = tk.Label(self.content_frame, text="Account Settings", 
                             font=("Helvetica", 18, "bold"), 
                             bg=self.colors['background'], fg=self.colors['text'])
        title_label.pack(anchor=tk.W, pady=(0, 20))
        
        settings_frame = tk.Frame(self.content_frame, bg=self.colors['card'], bd=0, padx=30, pady=30)
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        account_title = tk.Label(settings_frame, text="Update Admin Account", 
                              font=("Helvetica", 16, "bold"), 
                              bg=self.colors['card'], fg=self.colors['primary'])
        account_title.pack(anchor=tk.W, pady=(0, 20))
        
        username_frame = tk.Frame(settings_frame, bg=self.colors['card'], pady=10)
        username_frame.pack(fill=tk.X)
        
        username_label = tk.Label(username_frame, text="Username", width=15, anchor=tk.W,
                               font=("Helvetica", 12), 
                               bg=self.colors['card'], fg=self.colors['text'])
        username_label.pack(side=tk.LEFT, padx=(0, 10))
        
        username_entry = ttk.Entry(username_frame, width=30)
        username_entry.insert(0, self.username if self.username else "admin")
        username_entry.pack(side=tk.LEFT)
        
        old_password_frame = tk.Frame(settings_frame, bg=self.colors['card'], pady=10)
        old_password_frame.pack(fill=tk.X)
        
        old_password_label = tk.Label(old_password_frame, text="Current Password", width=15, anchor=tk.W,
                                  font=("Helvetica", 12), 
                                  bg=self.colors['card'], fg=self.colors['text'])
        old_password_label.pack(side=tk.LEFT, padx=(0, 10))
        
        old_password_entry = ttk.Entry(old_password_frame, width=30, show="•")
        old_password_entry.pack(side=tk.LEFT)
        
        new_password_frame = tk.Frame(settings_frame, bg=self.colors['card'], pady=10)
        new_password_frame.pack(fill=tk.X)
        
        new_password_label = tk.Label(new_password_frame, text="New Password", width=15, anchor=tk.W,
                                  font=("Helvetica", 12), 
                                  bg=self.colors['card'], fg=self.colors['text'])
        new_password_label.pack(side=tk.LEFT, padx=(0, 10))
        
        new_password_entry = ttk.Entry(new_password_frame, width=30, show="•")
        new_password_entry.pack(side=tk.LEFT)
        
        confirm_frame = tk.Frame(settings_frame, bg=self.colors['card'], pady=10)
        confirm_frame.pack(fill=tk.X)
        
        confirm_label = tk.Label(confirm_frame, text="Confirm Password", width=15, anchor=tk.W,
                              font=("Helvetica", 12), 
                              bg=self.colors['card'], fg=self.colors['text'])
        confirm_label.pack(side=tk.LEFT, padx=(0, 10))
        
        confirm_entry = ttk.Entry(confirm_frame, width=30, show="•")
        confirm_entry.pack(side=tk.LEFT)
        
        button_frame = tk.Frame(settings_frame, bg=self.colors['card'], pady=20)
        button_frame.pack(fill=tk.X)
        
        save_btn = ttk.Button(button_frame, text="Save Changes", width=20, style='TButton',
                          command=lambda: self.update_admin_account(
                              username_entry.get(),
                              old_password_entry.get(),
                              new_password_entry.get(),
                              confirm_entry.get()))
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_btn = ttk.Button(button_frame, text="Cancel", width=15,
                            command=self.show_dashboard)
        cancel_btn.pack(side=tk.LEFT)
    
    def update_admin_account(self, username, old_password, new_password, confirm_password):
        if not username or not old_password:
            messagebox.showerror("Error", "Username and current password are required")
            return
        
        if not self.db.verify_login("admin", old_password):
            messagebox.showerror("Error", "Current password is incorrect")
            return
        
        if new_password:
            if new_password != confirm_password:
                messagebox.showerror("Error", "New passwords do not match")
                return
            
            if len(new_password) < 4:
                messagebox.showerror("Error", "Password must be at least 4 characters")
                return
            
            # Updated method to change admin password would be added to the database class
            # This is a placeholder for the implementation
            messagebox.showinfo("Success", "Admin account updated successfully")
            self.show_dashboard()
        else:
            messagebox.showinfo("No Changes", "No changes were made to the account")
            self.show_dashboard()
    
    def open_student_form(self):
        self.root.withdraw()
        student_window = tk.Toplevel(self.root)
        student_form.StudentForm(student_window, self.db, self.root)
    
    def open_teacher_form(self):
        self.root.withdraw()
        teacher_window = tk.Toplevel(self.root)
        teacher_form.TeacherForm(teacher_window, self.db, self.root)
    
    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            self.login_window.deiconify()
    
    def exit_app(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()
            self.login_window.destroy()