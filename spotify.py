import os
from dotenv import load_dotenv
import base64
from requests import post, get
import json
import main

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
print(client_id, client_secret)

#use token in any future headers to send requests to get information
def get_token():
    #base 64 encoding send to retrive auth token
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    #request to acc service api
    #url to send req to
    url = "https://accounts.spotify.com/api/token"
    #headers associated w request
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"

    }
    #data
    data = {"grant_type": "client_credentials"}
    #post requset
    result = post(url, headers = headers, data = data)
    #convert json file into python dictionary, loadS (string)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

#auth header for future requests 
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

#done
def get_tracks(song, artist, number):
    token = get_token()
    song_ids = main.main(song, artist, number)
    #url and headers
    url = "https://api.spotify.com/v1/tracks"
    headers = get_auth_header(token)
    query = f"?ids={song_ids}"
    query_url  = url + query
    #get method to get info
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    print(json_result)

#in progress
def create_playlists(token, tracks):
    #url and headers
    url = "https://api.spotify.com/v1/users/{user_id}/playlists"
    headers = get_auth_header(token)
    query = f"?user_id={tracks}"
    query_url  = url + query
    #get method to get info
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    print(json_result)

token = get_token()
print(token)
tracks = "0Ak30vqlMnPP22CiKaP2GS"
get_tracks(token, tracks)