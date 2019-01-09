#!/usr/bin/env python3.5

# big thanks to this github repo https://github.com/mileshenrichs/spotify-playlist-generator/blob/master/generate.py
# how to get this program off the ground -> https://gist.github.com/iannase/38427b791a860a1f791b5fbba1791592
import sqlite3
import requests
from  bs4 import BeautifulSoup
import urllib.parse
import datetime
import json

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

from subprocess import call
import pprint
import AppleMusic

class jsonparser():
    def __init__(self, path=None):
        self.path = path
        self.jsondata = self.jsondatabase(self.path)
        self.keys = self.keysindata()
    def jsondatabase(self, path):
        jsonfile = open(path)
        jsonstr = jsonfile.read()
        return json.loads(jsonstr)
    def amountoftokens(self):
        return len(self.jsondata)
    # def appendtojson(self, jsondata):
    def keysindata(self):
        return [key for value, key in self.jsondata.items()]
    def getjsonkey(self, key):
        return self.jsondata[key]

class SpotifyPlaylist():
    def __init__(self, name=None, url=None):
        self.name = name
        self.url = url
        self.parser = jsonparser("config.json")

        self.username = self.parser.getjsonkey("username")
        self.secret = self.parser.getjsonkey("secret")
        self.client = self.parser.getjsonkey("client_id")
        client_credentials_manager = SpotifyClientCredentials(client_id=self.client, client_secret=self.secret)
        self.spotipyobj = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        token = util.prompt_for_user_token(username=self.username, scope='playlist-modify playlist-modify-private', client_id=self.client, client_secret=self.secret)
        self.spotipyPlaylist = spotipy.Spotify(auth=token)
    def playlistexists(self, name):
        # introduce logic to test for existence of playlist
        return True
    def getAccessToken(self):
        basicToken = self.parser.getjsonkey("encoded_basic_token")
        refreshToken = self.parser.getjsonkey("refresh_token")

        requestHeader = {'Authorization': 'Basic {}'.format(basicToken)}
        requestBody = {'grant_type': 'refresh_token', 'refresh_token': refreshToken}
        request = requests.post('https://accounts.spotify.com/api/token', headers=requestHeader, data=requestBody)
        requestJSON = request.json()
        newToken = requestJSON['access_token']
    def search(self, artist=None, track=None):
        result = self.spotipyobj.search(q="artist: {} track:{}".format(artist, track))
        if(len(result) == 0):
            return {}
        return result['tracks']['items'][0]
    def createNew(self, name, description="This is made from a bot I made!!!!!"):
        scope = 'playlist-modify-private playlist-modify-public playlist-read-private'
        # # token = util.prompt_for_user_token(self.username)
        token = util.prompt_for_user_token(username=self.username, scope='playlist-modify playlist-modify-private', client_id=self.client, client_secret=self.secret)
        # spotifyObj = spotipy.Spotify(auth=token)
        # spotifyObj.user_playlist_create(self.username, name, public=False)
        # print("Created a playlist!")
        url = "https://api.spotify.com/v1/users/%s/playlists" % (self.username)
        headers = {'Accept' : 'application/json', 'Authorization' : token, 'Content-Type' : "application/json"}
        data = "{\"name\":\"%s\",\"public\":true}" % (name)
        data = data.encode('UTF-8')
        r = requests.post(url, headers=headers, data=data)
    def addtoplaylist(self, track, play='5SgfDddDATgUpCXyEGWcuX'):
        scope = 'playlist-modify-private playlist-modify-public'
        token = util.prompt_for_user_token(self.username, scope)
        spoot = spotipy.Spotify(auth=token)
        spoot.user_playlist_add_tracks(self.username,play, track)
apple = AppleMusic.AppleMusicPlayist("https://itunes.apple.com/us/playlist/rock-hits-2007/pl.3af683127d6b4f21bd5a2f397b044f3b")
spot = SpotifyPlaylist()
apple.titular = "Jared is a beast"
for artist, track in apple.manifest.items():
    if(len(track) > 1):
        for item in track:
            res = spot.search(artist, item)
            spot.addtoplaylist(res['id'])
    else:
        res = spot.search(artist, track)
    spot.addtoplaylist(res['id'])
# a.genDatabase()
# spot.createNew("Jared made this!")
