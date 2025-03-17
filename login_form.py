# login_form.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import registration_form

class LoginForm:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.setup_ui()
    
    def setup_ui(self):
        self.root.title("Skills International - Login")
        self.root.geometry("400x350")  # Increased height to accommodate register button
        
        # Create frame for login
        login_frame = tk.Frame(self.root)
        login_frame.pack(pady=20)
        
        # Logo/Image
        # Load your image using Pillow
        # img = Image.open("assets/logo.png")
        # img = img.resize((150, 100))
        # self.logo = ImageTk.PhotoImage(img)
        # logo_label = tk.Label(login_frame, image=self.logo)
        # logo_label.pack(pady=10)
        
        # Title
        title_label = tk.Label(login_frame, text="Skills International", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Username
        username_label = tk.Label(login_frame, text="Username:")
        username_label.pack(anchor="w")
        self.username_entry = tk.Entry(login_frame, width=30)
        self.username_entry.pack(pady=5)
        
        # Password
        password_label = tk.Label(login_frame, text="Password:")
        password_label.pack(anchor="w")
        self.password_entry = tk.Entry(login_frame, width=30, show="*")
        self.password_entry.pack(pady=5)
        
        # Button frame
        button_frame = tk.Frame(login_frame)
        button_frame.pack(pady=10)
        
        # Clear button
        clear_button = tk.Button(button_frame, text="Clear", width=10, command=self.clear_fields)
        clear_button.grid(row=0, column=0, padx=5)
        
        # Login button
        login_button = tk.Button(button_frame, text="Login", width=10, command=self.login)
        login_button.grid(row=0, column=1, padx=5)
        
        # Exit button
        exit_button = tk.Button(button_frame, text="Exit", width=10, command=self.exit_app)
        exit_button.grid(row=0, column=2, padx=5)
        
        # Register section
        register_frame = tk.Frame(login_frame)
        register_frame.pack(pady=10)
        
        register_label = tk.Label(register_frame, text="Don't have an account?")
        register_label.pack(pady=5)
        
        register_button = tk.Button(register_frame, text="Register", width=15, command=self.open_register_form)
        register_button.pack()
    
    def clear_fields(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.username_entry.focus()
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if self.db.verify_login(username, password):
            messagebox.showinfo("Login Success", "Login successful!")
            self.root.withdraw()  # Hide login window
            self.open_registration_form()
        else:
            messagebox.showerror("Login Failed", "Invalid login credentials. Please check the Username and Password again and retry.")
    
    def open_registration_form(self):
        reg_window = tk.Toplevel(self.root)
        registration_form.RegistrationForm(reg_window, self.db, self.root)
    
    def open_register_form(self):
        # Create a new register account window
        register_window = tk.Toplevel(self.root)
        register_window.title("Register New Account")
        register_window.geometry("400x250")
        register_window.resizable(False, False)
        
        # Center the window
        window_width = 400
        window_height = 250
        screen_width = register_window.winfo_screenwidth()
        screen_height = register_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        register_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Registration form
        form_frame = tk.Frame(register_window)
        form_frame.pack(pady=20)
        
        title_label = tk.Label(form_frame, text="Create New Account", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Username
        username_label = tk.Label(form_frame, text="Username:")
        username_label.pack(anchor="w")
        new_username_entry = tk.Entry(form_frame, width=30)
        new_username_entry.pack(pady=5)
        
        # Password
        password_label = tk.Label(form_frame, text="Password:")
        password_label.pack(anchor="w")
        new_password_entry = tk.Entry(form_frame, width=30, show="*")
        new_password_entry.pack(pady=5)
        
        # Confirm password
        confirm_label = tk.Label(form_frame, text="Confirm Password:")
        confirm_label.pack(anchor="w")
        confirm_password_entry = tk.Entry(form_frame, width=30, show="*")
        confirm_password_entry.pack(pady=5)
        
        # Button frame
        button_frame = tk.Frame(form_frame)
        button_frame.pack(pady=10)
        
        # Create account button
        def create_account():
            username = new_username_entry.get()
            password = new_password_entry.get()
            confirm_password = confirm_password_entry.get()
            
            # Validate inputs
            if not username or not password:
                messagebox.showerror("Error", "Username and password are required.")
                return
            
            if password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match.")
                return
            
            # Check if username already exists
            if self.db.check_username_exists(username):
                messagebox.showerror("Error", "Username already exists. Please choose another.")
                return
            
            # Create the account
            if self.db.create_user(username, password):
                messagebox.showinfo("Success", "Account created successfully. You can now login.")
                register_window.destroy()
            else:
                messagebox.showerror("Error", "Failed to create account. Please try again.")
        
        create_button = tk.Button(button_frame, text="Create Account", width=15, command=create_account)
        create_button.grid(row=0, column=0, padx=5)
        
        # Cancel button
        cancel_button = tk.Button(button_frame, text="Cancel", width=10, command=register_window.destroy)
        cancel_button.grid(row=0, column=1, padx=5)
    
    def exit_app(self):
        if messagebox.askyesno("Exit Application", "Are you sure you want to exit?"):
            self.root.destroy()