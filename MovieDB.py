#Dealing with moviedb API for movie and tv show

import requests
import json
from Item import *

url = 'https://api.themoviedb.org/3'

#Poster URL for w185 picture
poster_url = 'https://image.tmdb.org/t/p/w185'
poster_url_w500 = 'https://image.tmdb.org/t/p/w500'

api_key = '214a06075aa82fef47cc3c4c2e61caf6'

def LiteSearchMovieWithID(database_id):
    #API url to search movie
    search_url = url + '/movie/' + database_id
    payload = {'api_key' : api_key}
    #Request the url
    r = requests.get(search_url,  params = payload)
    #Get details
    movie_details = json.loads(json.dumps(r.json()))
    #Add title and release date to a list then return it
    if(movie_details['release_date'] == None or movie_details['release_date'] == ''):
        movie_details['release_date'] = '1900-01-01'
    listOfDetails = [movie_details['title'], movie_details['release_date']]

    return listOfDetails

def FullSearchMovieWithID(database_id):
    #API url to search movie
    search_url = url + '/movie/' + database_id
    payload = {'api_key' : api_key}
    #Request the url
    r = requests.get(search_url,  params = payload)
    #Get details
    movie_details = json.loads(json.dumps(r.json()))
    #Add details to a list then return it
    listOfDetails = [movie_details['title'], str(movie_details['release_date']), 1, str(movie_details['original_title']), str(movie_details['original_language']), str(movie_details['overview'])
                     , poster_url_w500 + str(movie_details['poster_path'])]

    return listOfDetails

def LiteSearchTVWithID(database_id):
    #API url to search movie
    search_url = url + '/tv/' + database_id
    payload = {'api_key' : api_key}
    #Request the url
    r = requests.get(search_url,  params = payload)
    #Get details
    tv_details = json.loads(json.dumps(r.json()))
    #Add title, release date and # of episode to a list then return it
    if(tv_details['number_of_episodes'] == None):
        tv_details['number_of_episodes'] = 9999
    if(tv_details['first_air_date'] == None or tv_details['first_air_date'] == ''):
        tv_details['first_air_date'] = '1900-01-01'
    listOfDetails = [tv_details['name'], tv_details['first_air_date'], tv_details['number_of_episodes']]

    return listOfDetails

def FullSearchTVWithID(database_id):
    #API url to search movie
    search_url = url + '/tv/' + database_id
    payload = {'api_key' : api_key}
    #Request the url
    r = requests.get(search_url,  params = payload)
    #Get details
    tv_details = json.loads(json.dumps(r.json()))
    #Add details to a list then return it
    listOfDetails = [tv_details['name'], str(tv_details['first_air_date']), str(tv_details['number_of_episodes']), str(tv_details['original_name']),
                     str(tv_details['original_language']), str(tv_details['overview']), poster_url_w500 + str(tv_details['poster_path'])]

    return listOfDetails
    
def SearchMovie(title):
    #API url to search movie
    search_url = url+'/search/movie'
    payload = {'api_key' : api_key,  'query' : title}
    #Request the url
    r = requests.get(search_url,  params = payload)
    #Get the results of the search
    movie_details = json.loads(json.dumps(r.json()))['results']
    #Empty list of movie item objects
    mov_list = []
    #Create a movie item object based on the details of the json and append to the list
    for items in movie_details:
        mov_list.append(movie_item(str(items['id']),
                                   str(items['title']),
                                   str(items['popularity']),
                                   poster_url + str(items['poster_path']),
                                   1,
                                   str(items['original_language']),
                                   str(items['original_title']),
                                   str(items['overview']),
                                   str(items['release_date'])))
    return mov_list
    
def SearchTVShow(title):
    #API url to search tv shows
    search_url = url+'/search/tv'
    payload = {'api_key' : api_key,  'query' : title}
    #API url to get tv shows' details
    search_url_detail = url+'/tv/'
    payload_detail = {'api_key' : api_key}
    #Request URL
    r = requests.get(search_url,  params = payload)
    #Get the results of the search
    tv_details = json.loads(json.dumps(r.json()))['results']
    #Empty list of movie item objects
    tv_list = []
    #Loops through the shows, search the details for episode number and create movie item object
    for items in tv_details:
        new_r = requests.get(search_url_detail+str(items['id']), params=payload_detail)
        ep_number = json.loads(json.dumps(new_r.json()))['number_of_episodes']
        tv_list.append(movie_item(str(items['id']),
                                  str(items['name']),
                                  str(items['popularity']),
                                  poster_url + str(items['poster_path']),
                                  str(ep_number),
                                  str(items['original_language']),
                                  str(items['original_name']),
                                  str(items['overview']),
                                  str(items['first_air_date'])))
    return tv_list
