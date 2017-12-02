from flask import Flask, render_template, request, session, url_for, redirect
from MovieDB import *
from kitsu import *
from DBFunctionality import *

app = Flask(__name__)

@app.route('/')
def toMain():
    return redirect(url_for('index'))

@app.route('/index')
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    else:
        return render_template('index.html')

@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    username = request.form['username']
    password = request.form['password']

    if(checkLogin(username, password) == username):
        session['username'] = username
        return redirect(url_for('home'))
    else:
        message = 'Invalid password or username'
        return render_template('index.html', message=message)

@app.route('/register')
def register():
    if 'username' in session:
        return redirect(url_for('home'))
    else:
        return render_template('register.html')

@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    username = request.form['username']
    password = request.form['password']

    if(username == ''):
        message = 'Please enter an email'
        return render_template('register.html', message=message)

    if(insertNewLogin(username, password) == username):
        message = 'Register successfully!'
        return render_template('index.html', message=message)
    else:
        message = 'Email already in use'
        return render_template('register.html', message=message)
        

@app.route('/home')
def home():
    #Redirect back to main page if not logged in
    if 'username' not in session:
        return redirect(url_for('index'))
    
    else:
        return render_template('home.html')

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')
    
@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/movieresult', methods=['GET', 'POST'])
def movieResult():
    title = request.form['title']
    mov_list = SearchMovie(title)
    return render_template('movieresult.html', movies=mov_list)

@app.route('/tvresult', methods=['GET', 'POST'])
def tvResult():
    title = request.form['title']
    tv_list = SearchTVShow(title)
    return render_template('tvresult.html', movies=tv_list)

@app.route('/animeresult', methods=['GET', 'POST'])
def animeResult():
    title = request.form['title']
    ani_list = SearchAnime(title)
    return render_template('animeresult.html', movies=ani_list)

app.secret_key = 'some key that you will never guess'

if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)
