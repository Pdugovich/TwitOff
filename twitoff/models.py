"""These are my database models"""

from flask_sqlalchemy import SQLAlchemy

#import database, capital for global scope
DB = SQLAlchemy()

class User(DB.Model):
    """Twitter users that we analyze"""
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(15), nullable=False)

    def __repr__(self):
        # What will the user be represented as? 
        return '<User {}>'.format(self.name)


class Tweet(DB.Model):
    """The user's tweets from twitter"""
    id = DB.Column(DB.Integer, primary_key=True)
    text = DB.Column(DB.Unicode(280), nullable=False)
    # We don't need a reference from user to tweet, only tweet to user
    # Foreign key is to let it know it's from another column
    user_id = DB.Column(
        DB.Integer, DB.ForeignKey('user.id'), nullable=False)
    # Will not be stored in the database, but can be generated
    user = DB.relationship('User',backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return '<Tweet: {}>'.format(self.text)