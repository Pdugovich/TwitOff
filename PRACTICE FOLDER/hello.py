"""Minimal flask app"""

from flask import Flask, render_template

#make the application
app=Flask(__name__)

#make the route
#Using a default route
@app.route("/")

#Defining a function
def hello():
    return render_template('home.html')


#Creating another route
@app.route("/about")

def preds():
    return render_template('about.html')