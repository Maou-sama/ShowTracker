#Dealing with moviedb API for movie and tv show

import requests
import json
from item import *

url = 'https://api.themoviedb.org/3'

#Poster URL for w185 picture
poster_url = 'https://image.tmdb.org/t/p/w185'

api_key = '214a06075aa82fef47cc3c4c2e61caf6'

def SearchMovie(title):
    #API url to search movie
    search_url = url+'/search/movie'
    payload = {'api_key' : api_key,  'query' : title}
    #Request the url
    r = requests.get(search_url,  params = payload)
    
    print(r.status_code)
    #Get the results of the search
    movie_details = json.loads(json.dumps(r.json()))['results']
    #Empty list of movie item objects
    mov_list = []
    #Create a movie item object based on the details of the json and append to the list
    for items in movie_details:
        mov_list.append(movie_item(items['title'], items['popularity'], poster_url + str(items['poster_path']), 1, items['original_language'], items['original_title'], items['overview'], items['release_date']))
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
        tv_list.append(movie_item(items['name'], items['popularity'], poster_url + items['poster_path'], ep_number, items['original_language'], items['original_name'], items['overview'], items['first_air_date']))
    return tv_list