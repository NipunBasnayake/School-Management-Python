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
        
        logo_path = os.path.join("assets", "logo_white.png")
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
            {"text": "Reports", "icon": "report.png", "command": self.show_reports},
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
        
        card_width = 180
        card_height = 100
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
                          font=("Helvetica", 12), 
                          bg=card_data["color"], fg="white")
            title.pack(anchor=tk.W, padx=15, pady=(15, 5))
            
            value = tk.Label(card, text=card_data["value"], 
                          font=("Helvetica", 18, "bold"), 
                          bg=card_data["color"], fg="white")
            value.pack(anchor=tk.W, padx=15)
            
            if i == 0:
                self.student_count_label = value
            elif i == 1:
                self.teacher_count_label = value
        
        recent_frame = tk.Frame(self.content_frame, bg=self.colors['card'], bd=0)
        recent_frame.place(x=0, y=180, relwidth=0.65, relheight=0.6)
        
        recent_label = tk.Label(recent_frame, text="Recent Activities", 
                              font=("Helvetica", 14, "bold"), 
                              bg=self.colors['card'], fg=self.colors['text'])
        recent_label.pack(anchor=tk.W, padx=20, pady=15)
        
        activity_frame = tk.Frame(recent_frame, bg=self.colors['card'])
        activity_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        self.activity_tree = ttk.Treeview(activity_frame, columns=("Date", "User", "Action"), 
                                       show="headings", height=10)
        
        self.activity_tree.heading("Date", text="Date")
        self.activity_tree.heading("User", text="User")
        self.activity_tree.heading("Action", text="Action")
        
        self.activity_tree.column("Date", width=100)
        self.activity_tree.column("User", width=150)
        self.activity_tree.column("Action", width=250)
        
        self.activity_tree.pack(fill=tk.BOTH, expand=True)
        
        for i in range(5):
            date = datetime.now().strftime("%Y-%m-%d")
            self.activity_tree.insert("", "end", values=(date, "admin", "Logged into the system"))
        
        self.activity_tree.insert("", "end", values=(date, "admin", "Added new student: John Smith"))
        self.activity_tree.insert("", "end", values=(date, "admin", "Updated teacher: Jane Doe"))
        
        calendar_frame = tk.Frame(self.content_frame, bg=self.colors['card'], bd=0)
        calendar_frame.place(relx=0.7, y=180, relwidth=0.3, relheight=0.6)
        
        calendar_label = tk.Label(calendar_frame, text="Calendar", 
                                font=("Helvetica", 14, "bold"), 
                                bg=self.colors['card'], fg=self.colors['text'])
        calendar_label.pack(anchor=tk.W, padx=20, pady=15)
        
        today_date = datetime.now()
        month_year = today_date.strftime("%B %Y")
        month_label = tk.Label(calendar_frame, text=month_year, 
                             font=("Helvetica", 12), 
                             bg=self.colors['card'], fg=self.colors['text'])
        month_label.pack(pady=10)
        
        days_frame = tk.Frame(calendar_frame, bg=self.colors['card'])
        days_frame.pack(padx=15, pady=5)
        
        days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
        for day in days:
            day_label = tk.Label(days_frame, text=day, width=3, 
                              font=("Helvetica", 10), 
                              bg=self.colors['card'], fg=self.colors['text'])
            day_label.pack(side=tk.LEFT, padx=2)
        
        # Calendar grid (simplified)
        cal_frame = tk.Frame(calendar_frame, bg=self.colors['card'])
        cal_frame.pack(padx=15, pady=5)
        
        # Just a placeholder calendar display
        days_in_month = 30  # Simplified
        day_counter = 1
        
        for row in range(5):
            row_frame = tk.Frame(cal_frame, bg=self.colors['card'])
            row_frame.pack(fill=tk.X)
            
            for col in range(7):
                if (row == 0 and col < 3) or (day_counter > days_in_month):
                    day_btn = tk.Label(row_frame, text="", width=3, height=1,
                                    font=("Helvetica", 10), bg=self.colors['card'])
                else:
                    # Highlight today
                    if day_counter == today_date.day:
                        bg_color = self.colors['primary']
                        fg_color = "white"
                    else:
                        bg_color = self.colors['card']
                        fg_color = self.colors['text']
                    
                    day_btn = tk.Label(row_frame, text=str(day_counter), width=3, height=1,
                                    font=("Helvetica", 10), bg=bg_color, fg=fg_color)
                    day_counter += 1
                
                day_btn.pack(side=tk.LEFT, padx=2, pady=2)
    
    def load_dashboard_data(self):
        student_count = self.db.get_students_count()
        teacher_count = self.db.get_teachers_count()
        
        if hasattr(self, 'student_count_label'):
            self.student_count_label.config(text=str(student_count))
        
        if hasattr(self, 'teacher_count_label'):
            self.teacher_count_label.config(text=str(teacher_count))
    
    def show_reports(self):
        self.clear_content_frame()
        
        title_label = tk.Label(self.content_frame, text="Reports", 
                             font=("Helvetica", 18, "bold"), 
                             bg=self.colors['background'], fg=self.colors['text'])
        title_label.pack(anchor=tk.W, pady=(0, 20))
        
        reports_frame = tk.Frame(self.content_frame, bg=self.colors['card'], bd=0)
        reports_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        report_types = [
            {"title": "Student Reports", "desc": "View and export student data reports"},
            {"title": "Teacher Reports", "desc": "View and export teacher data reports"},
            {"title": "Financial Reports", "desc": "View financial statements and reports"},
            {"title": "Attendance Reports", "desc": "View student and teacher attendance reports"}
        ]
        
        for report in report_types:
            report_card = tk.Frame(reports_frame, bg=self.colors['card'], bd=0, 
                                height=80, padx=20, pady=15)
            report_card.pack(fill=tk.X, pady=1)
            
            report_title = tk.Label(report_card, text=report["title"], 
                                  font=("Helvetica", 14, "bold"), 
                                  bg=self.colors['card'], fg=self.colors['text'])
            report_title.pack(anchor=tk.W)
            
            report_desc = tk.Label(report_card, text=report["desc"], 
                                 font=("Helvetica", 10), 
                                 bg=self.colors['card'], fg=self.colors['light_text'])
            report_desc.pack(anchor=tk.W, pady=(5, 0))
            
            report_btn = ttk.Button(report_card, text="Generate", style="TButton")
            report_btn.pack(side=tk.RIGHT)
    
    def show_settings(self):
        self.clear_content_frame()
        
        title_label = tk.Label(self.content_frame, text="Settings", 
                             font=("Helvetica", 18, "bold"), 
                             bg=self.colors['background'], fg=self.colors['text'])
        title_label.pack(anchor=tk.W, pady=(0, 20))
        
        settings_frame = tk.Frame(self.content_frame, bg=self.colors['card'], bd=0)
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        settings_tabs = ttk.Notebook(settings_frame)
        
        general_tab = tk.Frame(settings_tabs, bg=self.colors['card'])
        account_tab = tk.Frame(settings_tabs, bg=self.colors['card'])
        system_tab = tk.Frame(settings_tabs, bg=self.colors['card'])
        
        settings_tabs.add(general_tab, text="General")
        settings_tabs.add(account_tab, text="Account")
        settings_tabs.add(system_tab, text="System")
        
        settings_tabs.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # General Settings
        general_title = tk.Label(general_tab, text="General Settings", 
                              font=("Helvetica", 14, "bold"), 
                              bg=self.colors['card'], fg=self.colors['text'])
        general_title.pack(anchor=tk.W, pady=(20, 10))
        
        theme_frame = tk.Frame(general_tab, bg=self.colors['card'], pady=10)
        theme_frame.pack(fill=tk.X)
        
        theme_label = tk.Label(theme_frame, text="Theme", width=15, anchor=tk.W,
                            font=("Helvetica", 12), 
                            bg=self.colors['card'], fg=self.colors['text'])
        theme_label.pack(side=tk.LEFT, padx=(0, 10))
        
        theme_combo = ttk.Combobox(theme_frame, values=["Light", "Dark", "System Default"], width=20)
        theme_combo.set("Light")
        theme_combo.pack(side=tk.LEFT)
        
        language_frame = tk.Frame(general_tab, bg=self.colors['card'], pady=10)
        language_frame.pack(fill=tk.X)
        
        language_label = tk.Label(language_frame, text="Language", width=15, anchor=tk.W,
                               font=("Helvetica", 12), 
                               bg=self.colors['card'], fg=self.colors['text'])
        language_label.pack(side=tk.LEFT, padx=(0, 10))
        
        language_combo = ttk.Combobox(language_frame, values=["English", "Spanish", "French", "German"], width=20)
        language_combo.set("English")
        language_combo.pack(side=tk.LEFT)
        
        # Account Settings
        account_title = tk.Label(account_tab, text="Account Settings", 
                              font=("Helvetica", 14, "bold"), 
                              bg=self.colors['card'], fg=self.colors['text'])
        account_title.pack(anchor=tk.W, pady=(20, 10))
        
        username_frame = tk.Frame(account_tab, bg=self.colors['card'], pady=10)
        username_frame.pack(fill=tk.X)
        
        username_label = tk.Label(username_frame, text="Username", width=15, anchor=tk.W,
                               font=("Helvetica", 12), 
                               bg=self.colors['card'], fg=self.colors['text'])
        username_label.pack(side=tk.LEFT, padx=(0, 10))
        
        username_entry = ttk.Entry(username_frame, width=30)
        username_entry.insert(0, self.username if self.username else "admin")
        username_entry.pack(side=tk.LEFT)
        
        old_password_frame = tk.Frame(account_tab, bg=self.colors['card'], pady=10)
        old_password_frame.pack(fill=tk.X)
        
        old_password_label = tk.Label(old_password_frame, text="Current Password", width=15, anchor=tk.W,
                                  font=("Helvetica", 12), 
                                  bg=self.colors['card'], fg=self.colors['text'])
        old_password_label.pack(side=tk.LEFT, padx=(0, 10))
        
        old_password_entry = ttk.Entry(old_password_frame, width=30, show="•")
        old_password_entry.pack(side=tk.LEFT)
        
        new_password_frame = tk.Frame(account_tab, bg=self.colors['card'], pady=10)
        new_password_frame.pack(fill=tk.X)
        
        new_password_label = tk.Label(new_password_frame, text="New Password", width=15, anchor=tk.W,
                                  font=("Helvetica", 12), 
                                  bg=self.colors['card'], fg=self.colors['text'])
        new_password_label.pack(side=tk.LEFT, padx=(0, 10))
        
        new_password_entry = ttk.Entry(new_password_frame, width=30, show="•")
        new_password_entry.pack(side=tk.LEFT)
        
        save_btn = ttk.Button(account_tab, text="Save Changes", style="TButton")
        save_btn.pack(pady=20)
        
        # System Settings
        system_title = tk.Label(system_tab, text="System Settings", 
                             font=("Helvetica", 14, "bold"), 
                             bg=self.colors['card'], fg=self.colors['text'])
        system_title.pack(anchor=tk.W, pady=(20, 10))
        
        backup_frame = tk.Frame(system_tab, bg=self.colors['card'], pady=10)
        backup_frame.pack(fill=tk.X)
        
        backup_label = tk.Label(backup_frame, text="Database Backup", width=15, anchor=tk.W,
                             font=("Helvetica", 12), 
                             bg=self.colors['card'], fg=self.colors['text'])
        backup_label.pack(side=tk.LEFT, padx=(0, 10))
        
        backup_btn = ttk.Button(backup_frame, text="Create Backup", style="TButton")
        backup_btn.pack(side=tk.LEFT)
        
        restore_frame = tk.Frame(system_tab, bg=self.colors['card'], pady=10)
        restore_frame.pack(fill=tk.X)
        
        restore_label = tk.Label(restore_frame, text="Restore Database", width=15, anchor=tk.W,
                              font=("Helvetica", 12), 
                              bg=self.colors['card'], fg=self.colors['text'])
        restore_label.pack(side=tk.LEFT, padx=(0, 10))
        
        restore_btn = ttk.Button(restore_frame, text="Restore from Backup", style="TButton")
        restore_btn.pack(side=tk.LEFT)
    
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