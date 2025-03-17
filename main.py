import tkinter as tk
import sys
import os
import logging
from pathlib import Path
from tkinter import messagebox

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('EduPro')

def ensure_directories():
    directories = ['assets', 'database', 'reports', 'backups']
    for directory in directories:
        dir_path = Path(directory)
        dir_path.mkdir(exist_ok=True)
        logger.info(f"Checked directory: {directory}")

def check_dependencies():
    try:
        from PIL import Image, ImageTk
        from tkcalendar import DateEntry
        logger.info("All dependencies are available")
        return True
    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        error_msg = f"Missing required dependency: {e}\n\n"
        error_msg += "Please install the required packages using:\n"
        error_msg += "pip install pillow tkcalendar"
        
        messagebox.showerror("Dependency Error", error_msg)
        return False

def create_default_assets():
    default_logo_path = Path("assets/logo.png")
    
    if not default_logo_path.exists():
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            img = Image.new('RGBA', (200, 200), color=(255, 255, 255, 0))
            d = ImageDraw.Draw(img)
            
            d.ellipse((20, 20, 180, 180), fill=(52, 152, 219, 255))
            
            try:
                font = ImageFont.truetype("arial.ttf", 80)
            except IOError:
                font = ImageFont.load_default()
                
            d.text((70, 55), "E", fill=(255, 255, 255, 255), font=font)
            img.save(default_logo_path)
            
            logger.info("Created default logo asset")
        except Exception as e:
            logger.error(f"Failed to create default asset: {e}")

def main():
    logger.info("Starting EduPro Academy Application")
    
    ensure_directories()
    
    if not check_dependencies():
        logger.error("Dependency check failed. Exiting application.")
        return
    
    create_default_assets()
    
    try:
        from database import Database
        from login_form import LoginForm
        
        root = tk.Tk()
        root.title("EduPro Academy")
        
        try:
            if os.path.exists("assets/icon.ico"):
                root.iconbitmap("assets/icon.ico")
        except Exception as e:
            logger.warning(f"Could not set application icon: {e}")
        
        try:
            db = Database()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            messagebox.showerror("Database Error", 
                               "Could not initialize database. Please check the error logs.")
            root.destroy()
            return
        
        login_form = LoginForm(root, db)
        logger.info("Login form initialized")
        
        root.resizable(False, False)
        
        window_width = 400
        window_height = 500
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        def on_closing():
            logger.info("Application closing")
            if db:
                db.close()
            root.destroy()
            
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        print("=" * 50)
        print("  EduPro Academy Management System v2.0")
        print("  Copyright © 2025 EduPro Academy")
        print("=" * 50)
        
        logger.info("Starting main event loop")
        root.mainloop()
        
    except Exception as e:
        logger.critical(f"Unexpected error: {e}", exc_info=True)
        messagebox.showerror("Error", 
                           f"An unexpected error occurred:\n{str(e)}\n\nPlease check the logs for details.")

if __name__ == "__main__":
    main()