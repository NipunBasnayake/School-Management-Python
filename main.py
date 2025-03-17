import tkinter as tk
import sys
import os
import logging
from pathlib import Path
from tkinter import messagebox

# Set up logging
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
    """Create necessary directories if they don't exist"""
    directories = ['assets', 'database', 'reports', 'backups']
    for directory in directories:
        dir_path = Path(directory)
        dir_path.mkdir(exist_ok=True)
        logger.info(f"Checked directory: {directory}")

def check_dependencies():
    """Check if all required dependencies are installed"""
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
    """Create default assets if they don't exist"""
    default_logo_path = Path("assets/logo.png")
    default_white_logo_path = Path("assets/logo_white.png")
    
    # Only create default logos if they don't exist
    if not default_logo_path.exists() or not default_white_logo_path.exists():
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create default logo
            img = Image.new('RGBA', (200, 200), color=(255, 255, 255, 0))
            d = ImageDraw.Draw(img)
            
            # Draw a circle
            d.ellipse((20, 20, 180, 180), fill=(52, 152, 219, 255))
            
            # Add text
            try:
                font = ImageFont.truetype("arial.ttf", 80)
            except IOError:
                font = ImageFont.load_default()
                
            d.text((70, 55), "E", fill=(255, 255, 255, 255), font=font)
            img.save(default_logo_path)
            
            # Create white logo version
            img_white = Image.new('RGBA', (200, 200), color=(255, 255, 255, 0))
            d_white = ImageDraw.Draw(img_white)
            d_white.ellipse((20, 20, 180, 180), fill=(255, 255, 255, 255))
            d_white.text((70, 55), "E", fill=(52, 152, 219, 255), font=font)
            img_white.save(default_white_logo_path)
            
            logger.info("Created default logo assets")
        except Exception as e:
            logger.error(f"Failed to create default assets: {e}")

def main():
    """Main application entry point"""
    logger.info("Starting EduPro Academy Application")
    
    # Ensure directories exist
    ensure_directories()
    
    # Check dependencies
    if not check_dependencies():
        logger.error("Dependency check failed. Exiting application.")
        return
    
    # Create default assets if needed
    create_default_assets()
    
    try:
        # Import dependencies here to avoid issues if they're missing
        from database import Database
        from login_form import LoginForm
        
        # Create the main window
        root = tk.Tk()
        root.title("EduPro Academy")
        
        # Set application icon if available
        try:
            if os.path.exists("assets/icon.ico"):
                root.iconbitmap("assets/icon.ico")
        except Exception as e:
            logger.warning(f"Could not set application icon: {e}")
        
        # Initialize database
        try:
            db = Database()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            messagebox.showerror("Database Error", 
                               "Could not initialize database. Please check the error logs.")
            root.destroy()
            return
        
        # Create login form
        login_form = LoginForm(root, db)
        logger.info("Login form initialized")
        
        # Set window properties
        root.resizable(False, False)  # Prevent resizing
        
        # Center the window on screen
        window_width = 400
        window_height = 500
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Set up a clean shutdown function
        def on_closing():
            logger.info("Application closing")
            if db:
                db.close()
            root.destroy()
            
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Display a splash message in console
        print("=" * 50)
        print("  EduPro Academy Management System v2.0")
        print("  Copyright © 2025 EduPro Academy")
        print("=" * 50)
        
        # Start the application
        logger.info("Starting main event loop")
        root.mainloop()
        
    except Exception as e:
        logger.critical(f"Unexpected error: {e}", exc_info=True)
        messagebox.showerror("Error", 
                           f"An unexpected error occurred:\n{str(e)}\n\nPlease check the logs for details.")

if __name__ == "__main__":
    main()