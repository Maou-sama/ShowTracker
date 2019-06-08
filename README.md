# ShowTracker
CS4523 Design Project 

Initial Release complete as of 12/6/17. Future implementations will be considered

A program designed for searching various type of shows(currently movies, tv shows, and anime)
and tracking it with user input (user has to manually input the episode watched).

A demo server is available at: https://oneandonlytracker.herokuapp.com/

## Dependencies:

-Python 3.x

-Flask

-mysqlclient

-requests

-gunicorn (only for production deployment)

## Instruction for running server:

-Deploy on herokuapp: clone/fork the repository, update DBFunctionality.py to point to your own DB and deploy

-Your own server: Install the dependencies, update DBFunctionality.py and deploy a dev/test build by running ShowTracker.py, i.e. $python ShowTracker.py
