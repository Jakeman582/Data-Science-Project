import os
import base64
from dotenv import load_dotenv
from requests import get, post
import json
import csv
from datetime import datetime
from time import sleep

def request_token(client_id, client_secret):

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

    json_result = json.loads(result.content)["tracks"]["items"]
    if len(json_result) != 0:
        return json_result[0]["id"]

    return json_result

def get_track_features(token, track_id):

    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = get_authorization_header(token)

    result = get(url, headers = headers)
    json_result = json.loads(result.content)

    return json_result

if __name__ == "__main__":

    load_dotenv()

    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    token = request_token(client_id, client_secret)
    
    # Get all the songs to search for
    songs = []
    with open("data/songs.csv") as file:
        song_reader = csv.reader(file, delimiter = "\t")
        for row in song_reader:
            songs.append([row[0], row[1]])
    
    # Tokens expire in an hour, so track how much time has elapsed
    time_start = datetime.now()

    with open("data/song_features.csv", "w") as file:

        song_writer = csv.writer(file, delimiter = "\t", lineterminator = "\n")
    
        # Query the Spotify API
        for song in songs[0:]:
            song_id = get_song_id(token, song[0], song[1])

            if len(song_id) != 0:
                song_features = get_track_features(token, song_id)
                song.append(song_features["acousticness"])
                song.append(song_features["danceability"])
                song.append(song_features["duration_ms"])
                song.append(song_features["energy"])
                song.append(song_features["instrumentalness"])
                song.append(song_features["key"])
                song.append(song_features["liveness"])
                song.append(song_features["loudness"])
                song.append(song_features["mode"])
                song.append(song_features["speechiness"])
                song.append(song_features["tempo"])
                song.append(song_features["time_signature"])
                song.append(song_features["valence"])
            else:
                song.append("")
                song.append("")
                song.append("")
                song.append("")
                song.append("")
                song.append("")
                song.append("")
                song.append("")
                song.append("")
                song.append("")
                song.append("")
                song.append("")
                song.append("")

            sleep(1.0)

            # Check if we're within 10 seconds of one hour to refresh the token
            if (datetime.now() - time_start).seconds > 3590:
                token = request_token(client_id, client_secret)
        
            song_writer.writerow(song)
