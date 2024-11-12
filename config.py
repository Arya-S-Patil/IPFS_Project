import os

class Config:
    """Configuration class for the Flask app."""
    
    # Secret key for session management
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')

    # SQLite database URI
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///files.db')

    # Disable track modifications to save memory
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # IPFS connection settings
    IPFS_HOST = 'localhost'
    IPFS_PORT = 5001
    IPFS_API_URL = f'http://{IPFS_HOST}:{IPFS_PORT}/api/v0'

    # Folder for temporary file storage
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Max file size: 16MB
