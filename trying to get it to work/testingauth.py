#!/usr/bin/env python3.5

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

scope = 'user-read-private user-read-playback-state user-modify-playback-state'
token = util.prompt_for_user_token("12164553253", scope)
spotifyObj = spotipy.Spotify(auth=token)
