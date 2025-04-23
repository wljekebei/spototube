import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic, OAuthCredentials
import os
from dotenv import load_dotenv

load_dotenv()

# spotify setup

scope = (
    "user-read-private user-read-email "
    "user-read-playback-state user-modify-playback-state "
    "user-read-currently-playing user-library-read user-library-modify "
    "playlist-read-private playlist-modify-private playlist-modify-public "
    "user-follow-read user-follow-modify user-read-recently-played "
    "user-top-read streaming app-remote-control"
)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, 
    client_id=os.getenv("SP_ID"), 
    client_secret=os.getenv("SP_SECRET"), 
    redirect_uri=os.getenv("SP_URI")))

# yt music setup

yt = YTMusic("oauth.json", oauth_credentials=OAuthCredentials(
    client_id=os.getenv("YT_ID"),
    client_secret=os.getenv("YT_SECRET")))

"""
тест

search_results = yt.search("Oasi Wonderll", filter='songs')
for res in search_results:
    print(res['title'], '-', res['artists'][0]['name'])
"""

# get tracks from spotify

def wholePlaylist(playlist_id):
    playlistTracks = sp.playlist_tracks(playlist_id='2iUyerShp2PjCiuEWXzSBB', limit=100)
    result = playlistTracks['items']

    while playlistTracks['next']:
        playlistTracks = sp.next(playlistTracks)
        result.extend(playlistTracks['items'])

    return result

"""
вывод всего плейлиста

for idx, item in enumerate(wholePlaylist('2iUyerShp2PjCiuEWXzSBB')):
    if (item['track'] != None):
        print(idx, item['track']['name'], '-', item['track']['artists'][0]['name'])
"""