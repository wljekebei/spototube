import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic, OAuthCredentials
import os
from dotenv import load_dotenv
from colorama import Fore

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
    redirect_uri=os.getenv("SP_URI"),
    cache_path= '.cache-lera'))

# yt music setup

yt = YTMusic("oauth.json", oauth_credentials=OAuthCredentials(
    client_id=os.getenv("YT_ID"),
    client_secret=os.getenv("YT_SECRET")))

def ytcreate():
    YTname = input(Fore.LIGHTBLUE_EX + "Enter name of the playlist: " + Fore.LIGHTMAGENTA_EX)
    YTdescription = input(Fore.LIGHTBLUE_EX + "Enter description of the playlist: " + Fore.LIGHTMAGENTA_EX)
    YTid = yt.create_playlist(YTname, YTdescription)
    return YTid

# get spotify playlist

def wholePlaylist(playlist_id):
    playlistTracks = sp.playlist_tracks(playlist_id=SPid, limit=100)
    result = playlistTracks['items']

    while playlistTracks['next']:
        playlistTracks = sp.next(playlistTracks)
        result.extend(playlistTracks['items'])

    print(Fore.LIGHTGREEN_EX + "\nTracks from Spotify were added to list!\n")

    return result

def wholeLiked():
    likedTracks = sp.current_user_saved_tracks()
    result = likedTracks['items']

    while likedTracks['next']:
        likedTracks = sp.next(likedTracks)
        result.extend(likedTracks['items'])

    print(Fore.LIGHTGREEN_EX + "\nTracks from Spotify were added to list!\n")

    return result

# add tracks to yt music

def addYT(tracks, playlist_id):
    decision = '0'
    i = 0
    for item in tracks:
        if item is not None and item['track'] is not None:
            searchRes = yt.search(f"{item['track']['name']} {item['track']['artists'][0]['name']}", limit=1, filter='songs')
            if searchRes is not None and len(searchRes) > 0:
                if decision != 'all':
                    decision = input(f"\n{Fore.WHITE}Do we add {Fore.YELLOW} {searchRes[0]['title']} {Fore.WHITE}by {Fore.CYAN} {searchRes[0]['artists'][0]['name']}? {Fore.WHITE}(y/n/all): ")
                if decision == 'y' or decision == 'all':
                    i += 1
                    yt.add_playlist_items(playlist_id, [searchRes[0]['videoId']])
                    print(f"{Fore.WHITE}{i}/{len(tracks)}: {Fore.YELLOW} {searchRes[0]['title']} {Fore.WHITE}by {Fore.CYAN} {searchRes[0]['artists'][0]['name']} {Fore.GREEN} was added! {Fore.WHITE}")
    print(f"{Fore.LIGHTGREEN_EX}{i} tracks were added!{Fore.WHITE}\n")

def getYtPlaylist(playlist_id):
    YTplaylist = yt.get_playlist(playlist_id)
    YTlist = YTplaylist['tracks']
    print(f"{Fore.LIGHTGREEN_EX}Got playlist named {Fore.YELLOW}{YTplaylist['title']}{Fore.LIGHTGREEN_EX}!")
    SPlist = wholePlaylist(SPid)

    if (YTplaylist['trackCount'] > 200):
        print("Your YT playlist already has >200 songs, approximated track which you should start with:")
        return SPlist [(YTplaylist['trackCount'] + 155):]
    
    matchIndex = -1
    matchTrack = None
    for ytitem in YTlist:
        for i, spitem in enumerate(SPlist):
            if spitem is not None and spitem['track'] is not None and spitem['track']['name'] is not None:
                if ytitem['title'] == spitem['track']['name']:
                    matchIndex = i
                    matchTrack = ytitem['title']
                    break

    if matchIndex != -1:
        print(f"{Fore.WHITE}Last found same track: {Fore.YELLOW}{matchTrack}{Fore.WHITE}\n")
        return SPlist[matchIndex + 1:]
    else:
        print(f"{Fore.RED}No matching tracks found!{Fore.WHITE}\n")
        return SPlist
    

if input(f"{Fore.WHITE}Adding from Spotify playlist or liked songs? (1/2): ") == '1':
    SPid = input(f"{Fore.WHITE}Enter Spotify playlist ID: ")
    # 2iUyerShp2PjCiuEWXzSBB
    res = wholePlaylist(SPid) # got all Spotify songs
else:
    res = wholeLiked()

if input(f"{Fore.WHITE}In reverse order? (y/n): ") == 'y':
    res = res[::-1]

if int(input(f"{Fore.WHITE}Add to playlist or create new? (1/2): ")) == 2:
    YTid = ytcreate() # playlist creation 
else:
    YTid = input(f"{Fore.WHITE}Enter YT Music playlist id: ")
    res = getYtPlaylist(YTid)
    # PLme4Sfi3EAQgWfuuIR_kOcrHYLBA1-qfH

if res:
    addYT(res, YTid) # adding everything to YTMusic
else:
    print("No new tracks to add!")