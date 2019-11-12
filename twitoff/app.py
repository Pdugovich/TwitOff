from flask import Flask
import click
from flask.cli import with_appcontext
from .models import *

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

    # creating a command to create a table with users and tweets
    @click.command(name='activate_team_richmond')
    # need to use with app context because the database config
    # is in the app, and I need that to add things to it
    @with_appcontext
    def activate_team_richmond():
        # wiping table remaking it
        DB.drop_all()
        DB.create_all()

        # assigning users to variables
        u1 = User(name='Richmond')
        t1 = Tweet(text='This is the first tweet')
        DB.session.add(u1)
        DB.session.add(t1)
        u1.tweets.append(t1)

        u2 = User(name='Patrick')
        t2 = Tweet(text='The second tweet')
        t2b = Tweet(text='Proof a single user can have multiple tweets')
        DB.session.add(u2)
        DB.session.add(t2)
        DB.session.add(t2b)
        u2.tweets.append(t2)
        u2.tweets.append(t2b)
        
        u3 = User(name='David')
        t3 = Tweet(text='The third tweet')
        DB.session.add(u3)
        DB.session.add(t3)
        u3.tweets.append(t3)
        
        u4 = User(name='Nick')
        t4 = Tweet(text='The fourth tweet')
        DB.session.add(u4)
        DB.session.add(t4)
        u4.tweets.append(t4)
        
        u5 = User(name='Raina')
        t5 = Tweet(text='The fifth tweet')
        DB.session.add(u5)
        DB.session.add(t5)
        u5.tweets.append(t5)
        
        u6 = User(name='Owen')
        t6 = Tweet(text='The sixth tweet')
        DB.session.add(u6)
        DB.session.add(t6)
        u6.tweets.append(t6)
        
        u7 = User(name='Trevor')
        t7 = Tweet(text='The seventh tweet')
        DB.session.add(u7)
        DB.session.add(t7)
        u7.tweets.append(t7)
        
        u8 = User(name='Vera')
        t8 = Tweet(text='The eigth tweet')
        DB.session.add(u8)
        DB.session.add(t8)
        u8.tweets.append(t8)
        
        u9 = User(name='Xander')
        t9 = Tweet(text='The ninth tweet')
        DB.session.add(u9)
        DB.session.add(t9)
        u9.tweets.append(t9)

        DB.session.commit()
    app.cli.add_command(activate_team_richmond)

    # @click.command(name='create_user')
    # @click.argument("user")
    # @with_appcontext
    # def create_user(user):
    #     user_exists = User.query.filter(User.name == f'{user}').first()
    #     if not user_exists:
    #         u1 = User(name=f'{user}')
    #         DB.session.add(u1)
    #         DB.session.commit()
    # app.cli.add_command(create_user)


    return app