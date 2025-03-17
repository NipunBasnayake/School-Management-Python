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
            'primary_dark': '#2980b9',
            'secondary': '#2ecc71',
            'accent': '#f39c12',
            'background': '#f5f5f5',
            'text': '#2c3e50',
            'light_text': '#7f8c8d',
            'border': '#e0e0e0'
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
        
        # Create a gradient background frame
        gradient_frame = tk.Frame(self.root, bg=self.colors['primary'], height=150)
        gradient_frame.pack(fill=tk.X)
        
        main_frame = tk.Frame(self.root, bg=self.colors['background'], padx=40, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Logo in the center of the gradient frame
        logo_path = "assets/logo.png"
        if os.path.exists(logo_path):
            try:
                logo_image = Image.open(logo_path)
                logo_image = logo_image.resize((120, 120), Image.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo_image)
                
                logo_label = tk.Label(gradient_frame, image=self.logo_photo, bg=self.colors['primary'])
                logo_label.place(relx=0.5, rely=0.5, anchor="center")
            except Exception as e:
                title_label = tk.Label(gradient_frame, text="EduPro Academy", 
                                     font=("Helvetica", 22, "bold"), bg=self.colors['primary'], 
                                     fg="white")
                title_label.place(relx=0.5, rely=0.5, anchor="center")
        else:
            title_label = tk.Label(gradient_frame, text="EduPro Academy", 
                                 font=("Helvetica", 22, "bold"), bg=self.colors['primary'], 
                                 fg="white")
            title_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Welcome text
        welcome_label = tk.Label(main_frame, text="Welcome Back", font=("Helvetica", 18, "bold"), 
                              bg=self.colors['background'], fg=self.colors['primary'])
        welcome_label.pack(pady=(0, 5))
        
        subtitle_label = tk.Label(main_frame, text="Sign in to continue", font=("Helvetica", 10), 
                               bg=self.colors['background'], fg=self.colors['light_text'])
        subtitle_label.pack(pady=(0, 25))
        
        # Username field with icon
        username_frame = tk.Frame(main_frame, bg=self.colors['background'])
        username_frame.pack(fill=tk.X, pady=5)
        
        username_label = tk.Label(username_frame, text="USERNAME", bg=self.colors['background'], 
                                fg=self.colors['text'], font=("Helvetica", 10, "bold"))
        username_label.pack(anchor=tk.W, pady=(5, 0))
        
        self.username_entry = ttk.Entry(username_frame, width=30, font=("Helvetica", 12),
                                    style='TEntry')
        self.username_entry.pack(fill=tk.X, pady=(2, 0), ipady=8)
        
        # Password field with icon
        password_frame = tk.Frame(main_frame, bg=self.colors['background'])
        password_frame.pack(fill=tk.X, pady=15)
        
        password_label = tk.Label(password_frame, text="PASSWORD", bg=self.colors['background'], 
                                fg=self.colors['text'], font=("Helvetica", 10, "bold"))
        password_label.pack(anchor=tk.W, pady=(5, 0))
        
        self.password_entry = ttk.Entry(password_frame, width=30, show="•", font=("Helvetica", 12),
                                    style='TEntry')
        self.password_entry.pack(fill=tk.X, pady=(2, 0), ipady=8)
        
        
        # Login button
        login_button = tk.Button(main_frame, text="LOGIN", font=("Helvetica", 12, "bold"),
                              bg=self.colors['primary'], fg="white", bd=0,
                              activebackground=self.colors['primary_dark'], activeforeground="white",
                              cursor="hand2", command=self.login)
        login_button.pack(fill=tk.X, pady=20, ipady=12)
        
        # Add hover effect to login button
        login_button.bind("<Enter>", lambda e: login_button.config(background=self.colors['primary_dark']))
        login_button.bind("<Leave>", lambda e: login_button.config(background=self.colors['primary']))
        
        # Create account option
        signup_frame = tk.Frame(main_frame, bg=self.colors['background'])
        signup_frame.pack(pady=10)
        
        no_account_label = tk.Label(signup_frame, text="Don't have an account?", 
                                  bg=self.colors['background'], fg=self.colors['light_text'])
        no_account_label.pack(side=tk.LEFT, padx=(0, 5))
        
        signup_btn = tk.Label(signup_frame, text="Sign Up", bg=self.colors['background'],
                           fg=self.colors['primary'], cursor="hand2", font=("Helvetica", 10, "bold"))
        signup_btn.pack(side=tk.LEFT)
        signup_btn.bind("<Button-1>", lambda e: self.show_create_account())
        
        # Add events
        self.username_entry.focus()
        self.username_entry.bind("<Return>", lambda event: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda event: self.login())
        
        # Footer
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
        window_height = 480
        screen_width = create_window.winfo_screenwidth()
        screen_height = create_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        create_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Header with gradient
        header_frame = tk.Frame(create_window, bg=self.colors['primary'], height=80)
        header_frame.pack(fill=tk.X)
        
        header_label = tk.Label(header_frame, text="Create New Account", 
                              font=("Helvetica", 18, "bold"), 
                              bg=self.colors['primary'], fg="white")
        header_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Form container
        form_frame = tk.Frame(create_window, bg=self.colors['background'], padx=40, pady=30)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Full name
        fullname_label = tk.Label(form_frame, text="FULL NAME", bg=self.colors['background'], 
                               fg=self.colors['text'], font=("Helvetica", 10, "bold"))
        fullname_label.pack(anchor=tk.W, pady=(10, 0))
        
        fullname_entry = ttk.Entry(form_frame, width=30, font=("Helvetica", 12),
                                style='TEntry')
        fullname_entry.pack(fill=tk.X, pady=(2, 15), ipady=8)
        
        # Username
        username_label = tk.Label(form_frame, text="USERNAME", bg=self.colors['background'], 
                               fg=self.colors['text'], font=("Helvetica", 10, "bold"))
        username_label.pack(anchor=tk.W, pady=(0, 0))
        
        new_username_entry = ttk.Entry(form_frame, width=30, font=("Helvetica", 12),
                                    style='TEntry')
        new_username_entry.pack(fill=tk.X, pady=(2, 15), ipady=8)
        
        # Password
        password_label = tk.Label(form_frame, text="PASSWORD", bg=self.colors['background'], 
                               fg=self.colors['text'], font=("Helvetica", 10, "bold"))
        password_label.pack(anchor=tk.W, pady=(0, 0))
        
        new_password_entry = ttk.Entry(form_frame, width=30, show="•", font=("Helvetica", 12),
                                    style='TEntry')
        new_password_entry.pack(fill=tk.X, pady=(2, 15), ipady=8)
        
        # Confirm Password
        confirm_label = tk.Label(form_frame, text="CONFIRM PASSWORD", bg=self.colors['background'], 
                              fg=self.colors['text'], font=("Helvetica", 10, "bold"))
        confirm_label.pack(anchor=tk.W, pady=(0, 0))
        
        confirm_password_entry = ttk.Entry(form_frame, width=30, show="•", font=("Helvetica", 12),
                                        style='TEntry')
        confirm_password_entry.pack(fill=tk.X, pady=(2, 25), ipady=8)
        
        # Terms acceptance
        terms_frame = tk.Frame(form_frame, bg=self.colors['background'])
        terms_frame.pack(fill=tk.X, pady=(0, 20))
        
        terms_var = tk.BooleanVar()
        terms_check = ttk.Checkbutton(terms_frame, text="I agree to the Terms & Conditions", 
                                    variable=terms_var, style='TCheckbutton')
        terms_check.pack(side=tk.LEFT)
        
        # Create Button
        create_button = tk.Button(form_frame, text="CREATE ACCOUNT", font=("Helvetica", 12, "bold"),
                               bg=self.colors['primary'], fg="white", bd=0,
                               activebackground=self.colors['primary_dark'], activeforeground="white",
                               cursor="hand2",
                               command=lambda: self.create_account(
                                   new_username_entry.get(),
                                   new_password_entry.get(),
                                   confirm_password_entry.get(),
                                   create_window,
                                   terms_var.get()))
        create_button.pack(fill=tk.X, ipady=12)
        
        # Add hover effect
        create_button.bind("<Enter>", lambda e: create_button.config(background=self.colors['primary_dark']))
        create_button.bind("<Leave>", lambda e: create_button.config(background=self.colors['primary']))
        
        # Cancel link
        cancel_frame = tk.Frame(form_frame, bg=self.colors['background'])
        cancel_frame.pack(pady=15)
        
        cancel_link = tk.Label(cancel_frame, text="Cancel", 
                            fg=self.colors['accent'], cursor="hand2",
                            bg=self.colors['background'], font=("Helvetica", 10, "bold"))
        cancel_link.pack()
        cancel_link.bind("<Button-1>", lambda e: create_window.destroy())
    
    def create_account(self, username, password, confirm_password, window, terms_accepted=False):
        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "All fields are required")
            return
        
        if not terms_accepted:
            messagebox.showerror("Error", "You must agree to the Terms & Conditions")
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