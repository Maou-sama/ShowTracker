from flask import Flask, render_template, request, session, url_for, redirect
from MovieDB import *
from kitsu import *

app = Flask(__name__)

@app.route('/')
def toMain():
    return redirect('/home')

@app.route('/home')
def home():
    #Redirect back to main page if not logged in
    if 'username' not in session:
        return redirect(url_for('main'))
    
    else:
        username = session['username']
        
        return render_template('home.html', username=username)