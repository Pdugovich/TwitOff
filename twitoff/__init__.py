"""Entry point for TwitOff."""
from .app import create_app

#APP is a global variable
APP = create_app()


# run this in terminal with
# set FLASK_APP=TWITOFF
# flask run