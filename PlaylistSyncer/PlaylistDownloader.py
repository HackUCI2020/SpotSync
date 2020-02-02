import sys
import os
import json
import webbrowser
from json.decoder import JSONDecodeError

import spotipy
import spotipy.util as util

def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print("   %d %32.32s %s" % (i, track['artists'][0]['name'],
            track['name']))

def printAndWriteTracks(tracks, file):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        artist_and_song = track['artists'][0]['name'] + " - " + track['name']
        print(artist_and_song)
        try:
            file.write(artist_and_song + "\n")
        except:
            pass


                 

# my user id: 21jarfouci4vnbo6z2ytnr6qa

username = '21jarfouci4vnbo6z2ytnr6qa'
scope = 'user-library-read'
client_id = '72bbb6fde66d465e9a5641fc7bf5dd9e'
client_secret = '26a648a8552e4dbd85af35e20a815d20'

anne_user = "anne.wang12"
anne_client_id = "a68602be8c9642b9afc83086371e1a05"
anne_client_secret = "fa5e0ae6c5834c68b820e183651a560f"

#os.remove(f".cache-{username}")
#get authorizaation token
try:
    token = util.prompt_for_user_token(username,scope,client_id= client_id, \
                                       client_secret= client_secret, \
                                       redirect_uri='https://google.com/')
    
except:
    os.remove(f".cache-{username}")
    print("uh oh")

print(token)
if token:
    SpotifyObject = spotipy.Spotify(auth=token)
    
    
    playlists = SpotifyObject.current_user_playlists(limit=3, offset=0)
    
    print("hi")
    for playlist in playlists['items']:
            print(playlist['owner']['id'])
            if playlist['owner']['id'] == username:
                print()
                playlist_name = playlist['name']
                file_name = playlist_name + ".txt"
                print ('  total tracks', playlist['tracks']['total'])
                results = SpotifyObject.playlist(playlist['id'],
                    fields="tracks,next")

                with open(file_name, "w") as file:
                    tracks = results['tracks']
                    #prints first 100 tracks of playlist
                    printAndWriteTracks(tracks, file)
                    
                    while tracks['next']:
                        tracks = SpotifyObject.next(tracks)
                        #prints next 100 tracks of playlists
                        printAndWriteTracks(tracks, file)
                



    '''
    q = "Downloaded"
    results = SpotifyObject.search(q, limit=1, offset=0, type='playlist', market=None)
    print(json.dumps(results, sort_keys=True, indent=4))
    '''
    
          
else:
    print("Can't get token for", username)


# print(json.dumps(VARIABLE, sort_keys=True, indent=4))
