#!/usr/bin/env python3.5

import sys
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pprint

if len(sys.argv) > 1:
    search_str = sys.argv[1]
else:
    search_str = 'Radiohead'

client_id = "d2697e8198c449f09abd2e0833f48dff"
client_secret = "862367c3080d49e782de1bd74641b876"

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

result = sp.search(q='artist: "A Day to Remember" track: "Life @ 11"')

pprint.pprint((result)['tracks']['items'])
# result = sp.search(search_str, limit=75)
# for items in result['tracks']['items']:
#     print(items['name'])
