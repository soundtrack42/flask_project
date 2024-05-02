from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
from dotenv import load_dotenv

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    """Construct the core application."""
    app = Flask(__name__)
    load_dotenv()  # Load environment variables from .env

    # Application Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Initialize Plugins with the application instance
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    return app

def setup_app(app):
    """Perform setup after app and db have been initialized."""
    with app.app_context():
        # Import here to avoid circular imports
        from .models import User  # Import User model here
        from .routes import init_routes

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))  # Adjust according to your user ID type if necessary

        db.create_all()  # Create database tables for our models
        init_routes(app)  # Setup routes for the application
