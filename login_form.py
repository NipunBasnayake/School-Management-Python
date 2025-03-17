import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
from PIL import Image, ImageTk
import os
import main_menu

class LoginForm:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.current_username = None
        self.colors = {
            'primary': '#3498db',
            'secondary': '#2ecc71',
            'accent': '#f39c12',
            'background': '#f5f5f5',
            'text': '#2c3e50',
            'light_text': '#7f8c8d'
        }
        self.setup_ui()
    
    def setup_ui(self):
        self.root.title("EduPro Academy - Login Portal")
        self.root.configure(bg=self.colors['background'])
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure('TEntry', 
                          background='white', 
                          foreground=self.colors['text'],
                          fieldbackground='white',
                          borderwidth=1,
                          relief='solid')
        
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
        
        login_frame = tk.Frame(self.root, bg=self.colors['background'], padx=30, pady=20)
        login_frame.pack(expand=True, fill=tk.BOTH)
        
        logo_frame = tk.Frame(login_frame, bg=self.colors['background'])
        logo_frame.pack(pady=15)
        
        logo_path = os.path.join("assets", "logo.png")
        if os.path.exists(logo_path):
            try:
                logo_image = Image.open(logo_path)
                logo_image = logo_image.resize((150, 150), Image.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo_image)
                
                logo_label = tk.Label(logo_frame, image=self.logo_photo, bg=self.colors['background'])
                logo_label.pack()
            except Exception as e:
                title_label = tk.Label(logo_frame, text="EduPro Academy", 
                                     font=("Helvetica", 24, "bold"), bg=self.colors['background'], 
                                     fg=self.colors['primary'])
                title_label.pack(pady=10)
        else:
            title_label = tk.Label(logo_frame, text="EduPro Academy", 
                                 font=("Helvetica", 24, "bold"), bg=self.colors['background'], 
                                 fg=self.colors['primary'])
            title_label.pack(pady=10)
        
        form_container = tk.Frame(login_frame, bg='white', bd=0, relief=tk.GROOVE, padx=30, pady=30)
        form_container.pack(pady=10, fill=tk.X)
        
        login_label = tk.Label(form_container, text="Welcome Back", font=("Helvetica", 16, "bold"), 
                              bg='white', fg=self.colors['primary'])
        login_label.pack(pady=(0, 20))
        
        username_frame = tk.Frame(form_container, bg='white')
        username_frame.pack(fill=tk.X, pady=5)
        
        username_label = tk.Label(username_frame, text="Username", bg='white', 
                                fg=self.colors['text'], font=("Helvetica", 10))
        username_label.pack(anchor=tk.W, pady=(5, 0))
        
        self.username_entry = ttk.Entry(username_frame, width=30, font=("Helvetica", 12),
                                    style='TEntry')
        self.username_entry.pack(fill=tk.X, pady=(2, 0), ipady=8)
        
        password_frame = tk.Frame(form_container, bg='white')
        password_frame.pack(fill=tk.X, pady=10)
        
        password_label = tk.Label(password_frame, text="Password", bg='white', 
                                fg=self.colors['text'], font=("Helvetica", 10))
        password_label.pack(anchor=tk.W, pady=(5, 0))
        
        self.password_entry = ttk.Entry(password_frame, width=30, show="•", font=("Helvetica", 12),
                                    style='TEntry')
        self.password_entry.pack(fill=tk.X, pady=(2, 0), ipady=8)
        
        button_frame = tk.Frame(form_container, bg='white')
        button_frame.pack(fill=tk.X, pady=(20, 10))
        
        login_button = tk.Button(button_frame, text="LOGIN", font=("Helvetica", 12, "bold"),
                              bg=self.colors['primary'], fg="white", bd=0,
                              activebackground=self.colors['secondary'], activeforeground="white",
                              cursor="hand2", command=self.login)
        login_button.pack(fill=tk.X, ipady=10)
        
        options_frame = tk.Frame(form_container, bg='white')
        options_frame.pack(fill=tk.X, pady=(10, 0))
        
        clear_button = tk.Label(options_frame, text="Clear Fields", bg='white',
                             fg=self.colors['accent'], cursor="hand2", font=("Helvetica", 10))
        clear_button.pack(side=tk.LEFT)
        clear_button.bind("<Button-1>", lambda e: self.clear_login_fields())
        
        create_account = tk.Label(options_frame, text="Create Account", bg='white',
                               fg=self.colors['primary'], cursor="hand2", font=("Helvetica", 10))
        create_account.pack(side=tk.RIGHT)
        create_account.bind("<Button-1>", lambda e: self.show_create_account())
        
        self.username_entry.focus()
        
        self.username_entry.bind("<Return>", lambda event: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda event: self.login())
        
        footer_frame = tk.Frame(self.root, bg=self.colors['background'], height=40)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        copyright_label = tk.Label(footer_frame, text="© 2025 EduPro Academy. All rights reserved.", 
                                 font=("Helvetica", 8), bg=self.colors['background'], 
                                 fg=self.colors['light_text'])
        copyright_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        version_label = tk.Label(footer_frame, text="v2.0", 
                               font=("Helvetica", 8), bg=self.colors['background'], 
                               fg=self.colors['light_text'])
        version_label.pack(side=tk.RIGHT, padx=20, pady=10)
    
    def clear_login_fields(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.username_entry.focus()
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Login Error", "Username and password are required")
            return
        
        if self.db.verify_login(username, password):
            self.current_username = username
            self.root.withdraw()
            self.open_main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials. Please try again.")
    
    def show_create_account(self):
        create_window = tk.Toplevel(self.root)
        create_window.title("Create Account - EduPro Academy")
        create_window.configure(bg=self.colors['background'])
        create_window.resizable(False, False)
        
        window_width = 400
        window_height = 350
        screen_width = create_window.winfo_screenwidth()
        screen_height = create_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        create_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Header
        header_label = tk.Label(create_window, text="Create New Account", 
                              font=("Helvetica", 18, "bold"), 
                              bg=self.colors['background'], fg=self.colors['primary'])
        header_label.pack(pady=(20, 30))
        
        # Form container
        form_frame = tk.Frame(create_window, bg='white', padx=30, pady=30)
        form_frame.pack(padx=20, fill=tk.X)
        
        # Username
        username_label = tk.Label(form_frame, text="Username", bg='white', 
                                fg=self.colors['text'], font=("Helvetica", 10))
        username_label.pack(anchor=tk.W, pady=(0, 0))
        
        new_username_entry = ttk.Entry(form_frame, width=30, font=("Helvetica", 12),
                                     style='TEntry')
        new_username_entry.pack(fill=tk.X, pady=(2, 10), ipady=8)
        
        # Password
        password_label = tk.Label(form_frame, text="Password", bg='white', 
                                fg=self.colors['text'], font=("Helvetica", 10))
        password_label.pack(anchor=tk.W, pady=(5, 0))
        
        new_password_entry = ttk.Entry(form_frame, width=30, show="•", font=("Helvetica", 12),
                                     style='TEntry')
        new_password_entry.pack(fill=tk.X, pady=(2, 10), ipady=8)
        
        # Confirm Password
        confirm_label = tk.Label(form_frame, text="Confirm Password", bg='white', 
                               fg=self.colors['text'], font=("Helvetica", 10))
        confirm_label.pack(anchor=tk.W, pady=(5, 0))
        
        confirm_password_entry = ttk.Entry(form_frame, width=30, show="•", font=("Helvetica", 12),
                                        style='TEntry')
        confirm_password_entry.pack(fill=tk.X, pady=(2, 20), ipady=8)
        
        # Create Button
        create_button = tk.Button(form_frame, text="CREATE ACCOUNT", font=("Helvetica", 12, "bold"),
                                bg=self.colors['primary'], fg="white", bd=0,
                                activebackground=self.colors['secondary'], activeforeground="white",
                                cursor="hand2",
                                command=lambda: self.create_account(
                                    new_username_entry.get(),
                                    new_password_entry.get(),
                                    confirm_password_entry.get(),
                                    create_window))
        create_button.pack(fill=tk.X, ipady=10)
        
        # Cancel link
        cancel_link = tk.Label(create_window, text="Cancel", 
                             fg=self.colors['accent'], cursor="hand2",
                             bg=self.colors['background'], font=("Helvetica", 10))
        cancel_link.pack(pady=15)
        cancel_link.bind("<Button-1>", lambda e: create_window.destroy())
    
    def create_account(self, username, password, confirm_password, window):
        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "All fields are required")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        if len(password) < 4:
            messagebox.showerror("Error", "Password must be at least 4 characters")
            return
        
        if self.db.check_username_exists(username):
            messagebox.showerror("Error", "Username already exists")
            return
        
        if self.db.create_user(username, password):
            messagebox.showinfo("Success", "Account created successfully. You can now login.")
            window.destroy()
        else:
            messagebox.showerror("Error", "Failed to create account. Please try again.")
    
    def open_main_menu(self):
        menu_window = tk.Toplevel(self.root)
        main_menu.MainMenu(menu_window, self.db, self.root, self.current_username)