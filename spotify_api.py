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

def get_song_id(token, artist, track):

    url = "https://api.spotify.com/v1/search"
    query = f"q={track}&artist={artist}"
    options = "type=track&market=US&limit=1&offset=0"

    search_url = url + "?" + query + "&" + options
    headers = get_authorization_header(token)

    result = get(search_url, headers = headers)
    json_result = json.loads(result.content)["tracks"]["items"][0]["id"]

    return json_result

def get_track_features(token, track_id):

    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = get_authorization_header(token)

    result = get(url, headers = headers)
    json_result = json.loads(result.content)

    print(json.dumps(json_result, indent = 4))

if __name__ == "__main__":

    load_dotenv()

    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    token = get_token(client_id, client_secret)

    song_id = get_song_id(token, "AC/DC", "Highway to Hell")
    get_track_features(token, song_id)