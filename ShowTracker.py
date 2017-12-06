from flask import Flask, render_template, request, session, url_for, redirect
from MovieDB import *
from Kitsu import *
from DBFunctionality import *

app = Flask(__name__)

@app.route('/')
def toMain():
    return redirect(url_for('index'))

#Index Page
@app.route('/index')
def index():
    #Go to home if there is an active user else render the page
    if 'username' in session:
        return redirect(url_for('home'))
    else:
        return render_template('index.html')

#Authenticate login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    username = request.form['username']
    password = request.form['password']

    #If user exist login and go to home else put out error message
    if(checkLogin(username, password) == username):
        session['username'] = username
        return redirect(url_for('home'))
    else:
        message = 'Invalid password or username'
        return render_template('index.html', message=message)

#Register Page
@app.route('/register')
def register():
    #Go to home if there is an active user else render the page
    if 'username' in session:
        return redirect(url_for('home'))
    else:
        return render_template('register.html')

#Authenticate Registration
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    username = request.form['username']
    password = request.form['password']

    #Error if username is blank since html does not prevent this
    if(username == ''):
        message = 'Please enter an email'
        return render_template('register.html', message=message)

    #Register in database if there isn't any other user with same email
    if(insertNewLogin(username, password) == username):
        message = 'Register successfully!'
        return render_template('index.html', message=message)
    else:
        message = 'Email already in use'
        return render_template('register.html', message=message)
        
#Home Page
@app.route('/home')
def home():
    #Redirect back to index if not logged in else render the page
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        return render_template('home.html')

#Delete user from active session when log out
@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')

#Search Page
@app.route('/search')
def search():
    #Redirect back to index if not logged in else render the page
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        return render_template('search.html')

#Search moviedb and get the results(display a maximum of 20 items)
@app.route('/movieresult', methods=['GET', 'POST'])
def movieResult():
    #Redirect back to index if not logged in
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        #Get the name from user input
        title = request.form['title']
        #Search movie then render the page with the list
        mov_list = SearchMovie(title)
        return render_template('movieresult.html', movies=mov_list)

#Search moviedb and get the results(display a maximum of 20 items)
@app.route('/tvresult', methods=['GET', 'POST'])
def tvResult():
    #Redirect back to index if not logged in
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        #Get the name from user input
        title = request.form['title']
        #Search movie then render the page with the list
        tv_list = SearchTVShow(title)
        return render_template('tvresult.html', movies=tv_list)

#Search kitsu and get the results(display a maximum of 20 items)
@app.route('/animeresult', methods=['GET', 'POST'])
def animeResult():
    #Redirect back to index if not logged in
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        #Get the name from user input
        title = request.form['title']
        #Search movie then render the page with the list
        ani_list = SearchAnime(title)
        return render_template('animeresult.html', movies=ani_list)

#Add the media to database to track
@app.route('/addMedia', methods=['GET', 'POST'])
def addMedia():
    #Redirect back to index if not logged in
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        #Get userID from database using user in session
        userID = getUserID(session['username'])
        #Get the specific database's id (the id from whichever database they come from) and the media type
        database_id = request.form['id']
        mediatype = request.form['type']
        #Insert to database depends on type
        if(mediatype == 'Movie'):
            detail_mov_list = LiteSearchMovieWithID(database_id)
            insertNewMovie(userID, database_id, detail_mov_list[0], 'Youtube', str(None), int(detail_mov_list[1].split('-')[0]))
        elif(mediatype == 'TVShow'):
            detail_tv_list = LiteSearchTVWithID(database_id)
            insertNewTVshow(userID, database_id, detail_tv_list[0], 'Youtube', int(detail_tv_list[1].split('-')[0]), int(detail_tv_list[2]), 0)
        elif(mediatype == 'Anime'):
            detail_anime_list = LiteSearchAnimeWithID(database_id)
            insertNewTVshow(userID, database_id, detail_anime_list[0], 'Crunchyroll', int(detail_anime_list[2].split('-')[0]), int(detail_anime_list[1]), 0, True)
        #Go to tracking page
        return redirect(url_for('tracking'))

#Tracking Page
@app.route('/tracking')
def tracking():
    #Redirect back to index if not logged in
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        #Get userID from database using user in session
        userID = getUserID(session['username'])
        #Get the movies and tv shows and animes that user are tracking from database
        resultMovie = getAllUserMovieRecords(userID)
        resultTV = getAllUserTVRecords(userID)
        resultAnime = getAllUserAnimeRecords(userID)    
        #Render the page with the list
        return render_template('tracker.html', movies=resultMovie, tvshows=resultTV, animes=resultAnime)

#Process update for show
@app.route('/updateProcess', methods=['GET', 'POST'])
def updateProcess():
    #Redirect back to index if not logged in
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        #Get userID from database using user in session
        userID = getUserID(session['username'])
        #Get the record ID and the episode user input
        recordID = request.form['id']
        episode = request.form['episode']
        if(episode != ''):
            #Update in database
            updateTVShow(userID, int(recordID), int(episode))
        #Go back to tracking page after done
        return redirect(url_for('tracking'))

#Process delete for show
@app.route('/deleteProcess', methods=['GET', 'POST'])
def deleteProcess():
    #Redirect back to index if not logged in
    if 'username' not in session:
        return redirect(url_for('index'))
    else:
        #Get userID from database using user in session
        userID = getUserID(session['username'])
        #Get the record ID
        recordID = request.form['id']
        #Delete from the database
        deleteRecord(userID, int(recordID))
        #Go back to tracking page after done
        return redirect(url_for('tracking'))
        
app.secret_key = 'some key that you will never guess'

if __name__ == "__main__":
    app.run('0.0.0.0', 5000, debug = True)
