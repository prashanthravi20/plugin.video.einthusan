import json
import time
import HTTPInterface
import requests
import re
from kodi_six import xbmc

##
# Gets the details when a movie id is passed.
#
# Returns a tuple as follows:
# 			(id, name, picture_url)
##


def get_movie_detail(movie_id):
    time.sleep(0.4)
    API_URL = 'http://www.einthusan.com/webservice/movie.php?id=' + \
        str(movie_id)
    html = HTTPInterface.http_get(API_URL)
    response_json = {}
    try:
        response_json = json.loads(html)
    except ValueError:
        print("Value Error: Error when decoding JSON")
        print(html)
    return response_json['movie_id'], response_json['movie'], response_json['cover']
##
# Returns a list of movie id for a specific filters
# returns json decoded of the response from the server
##


def apply_filter(filters):
    API_URL = 'http://www.einthusan.com/webservice/filters.php'
    result = HTTPInterface.http_post(API_URL, data=filters)
    response_json = {}
    try:
        response_json = json.loads(result)
    except ValueError:
        print("Value Error: Error when decoding JSON")
        print(result)
    return response_json


def get_options(attr, language):
    API_URL = 'http://www.einthusan.com/webservice/discovery.php'
    data = 'lang='+language

    html = HTTPInterface.http_post(API_URL, data=data)
    result = {}
    try:
        print(result)
        result = json.loads(html)
        return result['organize'][attr]['filtered']
    except KeyError:
        print("Key Error ")
    except ValueError:
        print("Value Error: Error when decoding JSON")
        print(html)
    return {}

##
# Returns the list of years available from the API endpoint.
##


def get_year_list(language):
    return get_options('Year', language)


def get_cast_helper(url, attr, language):
    referurl = url
    html = requests.get(url).text
    # xbmc.log(html, level=xbmc.LOGINFO)
    match = re.compile(
        '<a href="/movie/results/\?find=Cast.*?id=(.*?)&amp;lang=.*?role=(.*?)"><img.*?src="(.*?)">.*?<label>(.*?)</label>').findall(html)
    # Bit of a hack
    castlist = []
    for actorid, role, image, name in match:
        if 'http' not in image:
            image = 'http:' + image
        else:
            image = image
        if (role == attr):
            castlist.append(
                {'actorid': actorid, 'role': role, 'image': image, 'name': name})

    return castlist
    # s.close()
