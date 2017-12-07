#Dealing with kitsu API for anime

import requests
import json
from Item import *

url = 'https://kitsu.io/api/edge'

def LiteSearchAnimeWithID(database_id):
    #API url for searching
    search_url = url + '/anime'
    payload = {'filter[id]' : database_id}
    #Request the url
    r = requests.get(search_url, params=payload)
    #Get the results of the search
    anime_details = json.loads(json.dumps(r.json()))['data'][0]['attributes']
    #Put the title, episode # and release date in a list and return it
    if(anime_details['episodeCount'] == None):
        anime_details['episodeCount'] = 9999
    if(anime_details['startDate'] == None or anime_details['startDate'] == ''):
        anime_details['startDate'] = '1900-01-01'
    listOfDetails = [anime_details['canonicalTitle'], anime_details['episodeCount'], anime_details['startDate']]
    
    return listOfDetails

def FullSearchAnimeWithID(database_id):
    #API url for searching
    search_url = url + '/anime'
    payload = {'filter[id]' : database_id}
    #Request the url
    r = requests.get(search_url, params=payload)
    #Get the results of the search
    anime_details = json.loads(json.dumps(r.json()))['data'][0]['attributes']
    #Put details in a list and return it
    if 'ja_jp' in anime_details['titles']:
        listOfDetails = [anime_details['canonicalTitle'], str(anime_details['startDate']), str(anime_details['episodeCount']),
                         str(anime_details['titles']['ja_jp']), 'ja', str(anime_details['synopsis']), str(anime_details['posterImage']['large'])]

    else:
        listOfDetails = [anime_details['canonicalTitle'], str(anime_details['startDate']), str(anime_details['episodeCount']),
                         'None', 'ja', str(anime_details['synopsis']), str(anime_details['posterImage']['large'])]
    return listOfDetails

def SearchAnime(title):
    #API url for searching
    search_url = url + '/anime'
    payload = {'filter[text]' : title, 'page[limit]' : 20}
    #Request the url
    r = requests.get(search_url, params=payload)
    #Get the results of the search
    anime_details = json.loads(json.dumps(r.json()))['data']
    #Create a list of anime objects
    ani_list = []
    #Create an anime item object based on the details of the json and append to the list
    for items in anime_details:
        item_attributes = items['attributes']
        if 'ja_jp' in item_attributes['titles']:
            ani_list.append(anime_item(str(items['id']),
                                       str(item_attributes['canonicalTitle']),
                                       str(item_attributes['averageRating']),
                                       str(item_attributes['posterImage']['small']),
                                       str(item_attributes['episodeCount']),
                                       str(item_attributes['titles']['ja_jp']),
                                       str(item_attributes['synopsis']),
                                       str(item_attributes['startDate'])))
        else:
            ani_list.append(anime_item(str(items['id']),
                                       str(item_attributes['canonicalTitle']),
                                       str(item_attributes['averageRating']),
                                       str(item_attributes['posterImage']['small']),
                                       str(item_attributes['episodeCount']),
                                       None,
                                       str(item_attributes['synopsis']),
                                       str(item_attributes['startDate'])))
        
    return ani_list
