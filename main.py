# main.py
import tkinter as tk
import sys
import os
from database import Database
from login_form import LoginForm

def main():
    # Create the main window
    root = tk.Tk()
    
    # Set application icon if available
    try:
        if os.path.exists("assets/icon.ico"):
            root.iconbitmap("assets/icon.ico")
    except:
        pass
    
    # Initialize database
    db = Database()
    
    # Create login form
    login_form = LoginForm(root, db)
    
    # Set window properties
    root.resizable(False, False)  # Prevent resizing
    
    # Center the window on screen
    window_width = 400
    window_height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # Start the application
    root.mainloop()
    
    # Close database connection when application ends
    db.close()

if __name__ == "__main__":
    main()