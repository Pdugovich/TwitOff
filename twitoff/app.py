from decouple import config
from flask import Flask, render_template, request
import click
from flask.cli import with_appcontext
from .models import DB, Tweet, User
from .twitter import add_user_and_tweets

#Now we make the app factory

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)

    #add our config
    # I need a LOT OF info about what's going on here
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    # Setting a config to prevent the error that comes up with flask run
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # setting another config to show more details about server errors
    app.config['ENV'] = config('ENV')

    #now have the database know about the app
    DB.init_app(app)

    @app.route('/')
    def hello():
        users = User.query.all()
        return render_template('base.html', title='Homepage', users=users)
    
    @app.route('/<name>')
    def user(name):
        name = name
        add_user_and_tweets(name)
        tweets = User.query.filter(User.name == name).first().tweets
        return render_template('user.html', title=name, tweets=tweets)



    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset',users=[])

    return app