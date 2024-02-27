from dotenv import load_dotenv
from requests import post, get
import os
import base64
import json
import random

import requests, json

#import os
#import asyncio
#from shazamio import Shazam

print('Get current working directory : ', os.getcwd())

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

#async def main():
#  shazam = Shazam()
#  out = await shazam.recognize_song(r'C:\Users\jnhol\Downloads\shazam_test\data\smooth_5secs.mp3')
#  print(out)

#loop = asyncio.get_event_loop()
#loop.run_until_complete(main())

# Gets token for requesting spotify data
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = { 
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_headers(token):
    return {"Authorization": "Bearer " + token}

# Searches for artist and returns their json data 
def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_headers(token)

    query = "?q="+artist_name+"&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if  len(json_result) == 0:
        print("No artist man soz")
        return None

    return json_result[0]

# Searches for specific song and returns thats songs data
def search_for_song(token, song_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_headers(token)

    query = "?q=" + song_name + "&type=track&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["tracks"]["items"]
    if len(json_result) == 0:
        print("noor sorryyy")
        return None
    
    return json_result[0]

# Uses song id to find audio ANALYSIS
def audio_analysis(token, song_id):
    url = "https://api.spotify.com/v1/audio-analysis/"+song_id
    headers = get_auth_headers(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["track"]
    return json_result

# ---- CHECK API FOR DIFFERENCE BETWEEN THESE ------

# Uses song id to find audio FEATURES
def audio_features(token, song_id):
    url = "https://api.spotify.com/v1/audio-features/"+song_id
    headers = get_auth_headers(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

# prints song features for easy seeing   
def print_song_features(token, song_name):
    track = search_for_song(token, song_name)
    track_id = track["id"]

    audio_analy = audio_analysis(token, track_id)
    audio_feats = audio_features(token, track_id)
    print()
    print("Loud: " + str(audio_analy["loudness"]))
    print("Tempo: " + str(audio_analy["tempo"]))
    print("Tempo Conf: " + str(audio_analy["tempo_confidence"]))
    print("Time Signature: " + str(audio_analy["time_signature"]))
    print()
    print("Danceability: " + str(audio_feats["danceability"]))
    print("Valence: " + str(audio_feats["valence"]))
    print("Energy: " + str(audio_feats["energy"]))


# Searches for artist and returns their list of top tracks 
#def get_songs_by_artist(token, artist_id):
#    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=BR"
#    headers = get_auth_headers(token)
#    result = get(url, headers=headers)
#    json_result = json.loads(result.content)["tracks"]
#    return json_result
