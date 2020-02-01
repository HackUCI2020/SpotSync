import sys
import os
import json
import webbrowser
from json.decoder import JSONDecodeError

import spotipy
import spotipy.util as util

# my user id: h21jarfouci4vnbo6z2ytnr6qa?si=ghWKTiLPQNqx2Dh2YnTuyg

username = '21jarfouci4vnbo6z2ytnr6qa?si=ghWKTiLPQNqx2Dh2YnTuyg'

scope = 'user-library-read'

#get authorizaation token
try:
    token = util.prompt_for_user_token(username,scope,client_id='72bbb6fde66d465e9a5641fc7bf5dd9e', \
                                       client_secret='26a648a8552e4dbd85af35e20a815d20', \
                                       redirect_uri='https://google.com/')
except:
    os.remove(f".cache-{username}")

if token:
    SpotifyObject = spotipy.Spotify(auth=token)
    
    user = SpotifyObject.current_user()
    print(json.dumps(user, sort_keys=True, indent=4))

    playlists = SpotifyObject.current_user_playlists(limit=1, offset=0)
    print(json.dumps(playlists, sort_keys=True, indent=4))

    

    
          
else:
    print("Can't get token for", username)


# print(json.dumps(VARIABLE, sort_keys=True, indent=4))
