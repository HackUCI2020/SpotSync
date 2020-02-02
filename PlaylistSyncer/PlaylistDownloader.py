import sys
import os
import pathlib
import json
import webbrowser
from json.decoder import JSONDecodeError

import spotipy
import spotipy.util as util

# deprecated
""""
def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print("   %d %32.32s %s" % (i, track['artists'][0]['name'],
            track['name']))
"""


credentials = {
    "username": '21jarfouci4vnbo6z2ytnr6qa',
    "scope": 'user-library-read',
    "client_id": '72bbb6fde66d465e9a5641fc7bf5dd9e',
    "client_secret": '26a648a8552e4dbd85af35e20a815d20'
}

def get_token(credentials=credentials):
    return util.prompt_for_user_token(credentials["username"],
                                      credentials['scope'],
                                      client_id=credentials["client_id"],
                                      client_secret=credentials["client_secret"],
                                      redirect_uri='https://google.com/')


def safe_capture_token(credentials=credentials):
    try:
        return get_token()
    except:
        os.remove(f".cache-{credentials['username']}")
        print("failed to retrieve token")


def get_playlists(SpotifyObject):
    playlists = SpotifyObject.current_user_playlists(limit=3, offset=0)
    return playlists['items']


def write_all_tracks(SpotifyObject, tracks, file_name, dir_path=''):
    file_name = dir_path + file_name
    file = pathlib.PurePath(file_name)
    write_tracks(tracks, file)
    while tracks['next']:
        tracks = SpotifyObject.next(tracks)
        write_tracks(tracks, file)


def write_tracks(tracks, file):
    with open(file, "w") as file:
        for i, item in enumerate(tracks['items']):
            track = item['track']
            artist_and_song = track['artists'][0]['name'] + " - " + track['name']
            try:
                file.write(artist_and_song + "\n")
            except UnicodeEncodeError:  # song cannot be encoded with utf-8
                pass


def download_playlists(file_path=''):
    token = safe_capture_token()
    if not token:
        print("Can't get token for", credentials['username'])
    else:
        SpotifyObject = spotipy.Spotify(auth=token)
        for playlist in get_playlists(SpotifyObject):
            if playlist['owner']['id'] == credentials['username']:
                file_name = playlist['name'] + ".txt"
                print (f'{file_name}: \ttotal tracks {playlist["tracks"]["total"]}')
                results = SpotifyObject.playlist(playlist['id'], fields="tracks,next")
                write_all_tracks(SpotifyObject, results['tracks'], file_name, file_path)


if __name__ == "__main__":
    download_playlists("../PlaylistParser/playlists/")
