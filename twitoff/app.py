from flask import Flask
from .models import DB

#Now we make the app factory

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)

    #add our config
    # I need a LOT OF info about what's going on here
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    #now have the database know about the app
    DB.init_app(app)

    @app.route('/')
    def hello():
        return 'Welcome to TwitOff!'

    return app