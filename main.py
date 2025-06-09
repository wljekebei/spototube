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

# playlists id's and creation

SPid = '2iUyerShp2PjCiuEWXzSBB'

def ytcreate():
    YTname = input("Enter name of the playlist: ")
    YTdescription = input("Enter description of the playlist: ")
    YTid = yt.create_playlist(YTname, YTdescription)
    return YTid

# get spotify playlist

def wholePlaylist(playlist_id):
    playlistTracks = sp.playlist_tracks(playlist_id=SPid, limit=100)
    result = playlistTracks['items']

    while playlistTracks['next']:
        playlistTracks = sp.next(playlistTracks)
        result.extend(playlistTracks['items'])

    print("Tracks from Spotify were added to list!\n")

    return result


# add tracks to yt music

def addYT(tracks, playlist_id):
    decision = '0'
    for item in tracks:
        searchRes = yt.search(f"{item['track']['name']} {item['track']['artists'][0]['name']}", limit=1, filter='songs')
        if decision != 'all':
            decision = input(f"\nDo we add {searchRes[0]['title']} by {searchRes[0]['artists'][0]['name']}? (y/n/all): ")
        if decision == 'y' or decision == 'all':
            yt.add_playlist_items(playlist_id, [searchRes[0]['videoId']])
            print(f"{searchRes[0]['title']} by {searchRes[0]['artists'][0]['name']} was added!")


YTid = ytcreate() # playlist creation
res = wholePlaylist(id) # got all Spotify songs
addYT(res, YTid) # adding everything to YTMusic