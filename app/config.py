import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Application configuration for local MySQL on Azure Ubuntu VM
    All database settings are loaded from environment variables (.env file)
    """
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey123")
    
    # Database Configuration - Local MySQL on Azure VM
    # For local MySQL on same VM, use: localhost or 127.0.0.1
    # These defaults match the .env file configuration
    DB_HOST = os.getenv("DB_HOST", "localhost")  # Use 'localhost' for local MySQL on same VM
    DB_PORT = int(os.getenv("DB_PORT", 3306))
    DB_USER = os.getenv("DB_USER", "appuser")  # Default matches .env
    DB_PASSWORD = os.getenv("DB_PASSWORD", "StrongPassword@123")  # Default matches .env
    DB_NAME = os.getenv("DB_NAME", "appdb")  # Default matches .env
    JWT_ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

    # Absolute folder path for image uploads inside your app
    APP_ROOT = os.path.abspath(os.path.dirname(__file__))  # Absolute path of app folder
    UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/upload_image')
    
    # OpenAI API Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")  # Updated: gpt-4-vision-preview is deprecated. Use gpt-4o or gpt-4-turbo