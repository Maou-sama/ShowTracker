from flask import Flask, render_template, request, session, url_for, redirect
from MovieDB import *
from kitsu import *

app = Flask(__name__)

@app.route('/')
def toMain():
    return redirect('/search')

@app.route('/home')
def home():
    #Redirect back to main page if not logged in
    if 'username' not in session:
        return redirect(url_for('main'))
    
    else:
        username = session['username']
        
        return render_template('home.html', username=username)
    
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