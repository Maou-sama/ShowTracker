#Dealing with kitsu API for anime

import requests
import json
from item import *

url = 'https://kitsu.io/api/edge'

def SearchAnime(title):
    #API url for searching
    search_url = url + '/anime'
    payload = {'filter[text]' : title, 'page[limit]' : 20}
    #Request the ur;
    r = requests.get(search_url, params=payload)
    #Get the results of the search
    anime_details = json.loads(json.dumps(r.json()))['data']
    #Create a list of anime objects
    ani_list = []
    #Create an anime item object based on the details of the json and append to the list
    for items in anime_details:
        item_attributes = items['attributes']
        if 'ja_jp' in item_attributes['titles']:
            ani_list.append(anime_item(item_attributes['canonicalTitle'], item_attributes['averageRating'], item_attributes['posterImage']['small'], item_attributes['episodeCount'], item_attributes['titles']['ja_jp'], item_attributes['synopsis'], item_attributes['startDate']))
        else:
            ani_list.append(anime_item(item_attributes['canonicalTitle'], item_attributes['averageRating'], item_attributes['posterImage']['small'], item_attributes['episodeCount'], None, item_attributes['synopsis'], item_attributes['startDate']))
        
    return ani_list