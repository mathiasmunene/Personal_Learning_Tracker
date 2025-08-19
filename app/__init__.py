from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Initialize extensions (but don't attach to app yet)
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    """Application factory function"""
    # Create Flask app instance
    app = Flask(__name__)
    
    # Load configuration from Config class
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Import and register blueprints (routes)
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app