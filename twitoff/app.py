"""Build app factor and do routes and configurations"""

from decouple import config
from dotenv import load_dotenv
from flask import Flask, render_template, request
from .models import DB, Tweet, User
from .twitter import add_or_update_user
from .predict import predict_user

load_dotenv()
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
    
    #adding in a new route to add/get users
    @app.route('/user', methods=['POST']) #uses form
    @app.route('/user/<name>', methods=['GET']) #needs parameter
    def user(name=None, message=""):
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = "User {} successfully added!".format(name)
                tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = "Error adding {}: {}".format(name,e)
            tweets = []
        return render_template('user.html', title=name, tweets=tweets,
                               message=message)


    #adding in a route for predictions
    @app.route('/compare', methods=['POST'])
    def compare(message=''):
        user1, user2 = sorted([request.values['user1'],
                               request.values['user2']])
        if user1 == user2:
            message = 'Cannot compare a user to themselves'
        else:
            prediction = predict_user(user1, user2, request.values['tweet_text'])
            message = '"{}" is more likely to be said by {} than {}'.format(
                request.values['tweet_text'], user1 if prediction else user2,
                user2 if prediction else user1
            )
        return render_template('prediction.html', title='Prediction',message=message)


    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset',users=[])

    return app