import os
import base64
from dotenv import load_dotenv
from requests import get, post
import json

def get_token(client_id, client_secret):
    authorization_string = client_id + ":" + client_secret
    authorization_bytes = authorization_string.encode("utf-8")
    authorization_base64 = str(base64.b64encode(authorization_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + authorization_base64, 
        "Content-Type": "application/x-www-form-urlencoded", 
    }
    data = {"grant_type": "client_credentials"}

    result = post(url, headers=headers, data = data)

    json_result = json.loads(result.content)

    token = json_result["access_token"]

    return token

def get_authorization_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):

    url = "https://api.spotify.com/v1/search"
    headers = get_authorization_header(token)
    query = f"q={artist_name}&type=artist&limit=1"

    query_url = url + "?" + query

    result = get(query_url, headers = headers)
    json_result = json.loads(result.content)["artists"]["items"]

    if len(json_result) == 0:
        print("Artist not found")
        return None
    
    return json_result[0]

    #print(json.dumps(json_result, indent = 4))

def get_top_tracks(token, artist_id):

    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_authorization_header(token)
    result = get(url, headers = headers)

    json_result = json.loads(result.content)["tracks"]

    return json_result

def get_song_id(token, artist, track):

    url = "https://api.spotify.com/v1/search"
    query = f"q={track}&artist={artist}"
    options = "type=track&market=US&limit=1&offset=0"

    search_url = url + "?" + query + "&" + options
    headers = get_authorization_header(token)

    result = get(search_url, headers = headers)
    json_result = json.loads(result.content)["tracks"]["items"][0]["id"]

    return json.dumps(json_result, indent = 4)

if __name__ == "__main__":

    load_dotenv()

    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    token = get_token(client_id, client_secret)
    result = search_for_artist(token, "ACDC")
    artist_id = result["id"]
    songs = get_top_tracks(token, artist_id)
    
    #for index, song in enumerate(songs):
        #print(f"{index + 1}.) {song['name']}")
    
    song_name = get_song_id(token, "AC/DC", "Highway%20to%20Hell")
    print(song_name[1:-1])