import os
from datetime import timedelta

# Get the base directory of our project
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key for session management security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-very-secret-key-here'
    
    # Database configuration - using SQLite for simplicity
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'learning_tracker.db')
    
    # Disable modification tracking to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session lifetime set to 7 days
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)