#!/usr/bin/env python3.5

# big thanks to this github repo https://github.com/mileshenrichs/spotify-playlist-generator/blob/master/generate.py
# how to get this program off the ground -> https://gist.github.com/iannase/38427b791a860a1f791b5fbba1791592

# backend requests made to the servers
import sqlite3
import requests
from  bs4 import BeautifulSoup
import urllib.parse


# working with spotify
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import oauth2

# working on the local machine
from subprocess import call
import pprint

# Libraries that I wrote
import AppleMusic
from JSONParser import jsonparser

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

    def playlistexists(self, name):
        # introduce logic to test for existence of playlist
        return True
    def retrieve_recent_token(self):
        with open("tokens", 'r') as file:
            newToken = self.token = file.readline()
            file.close()
        return newToken
    def getAccessToken(self):
        # basicToken = self.parser.getjsonkey("encoded_basic_token")
        # refreshToken = self.parser.getjsonkey("refresh_token")
        #
        # requestHeader = {'Authorization': 'Basic {}'.format(basicToken)}
        # requestBody = {'grant_type': 'refresh_token', 'refresh_token': refreshToken}
        # request = requests.post('https://accounts.spotify.com/api/token', headers=requestHeader, data=requestBody)
        # requestJSON = request.json()
        # newToken = requestJSON['access_token']
        # return newToken
        sp_oauth = oauth2.SpotifyOAuth(client_id=self.client, client_secret=self.secret, redirect_uri="http://localhost:8888",scope="playlist-modify-public playlist-read-private user-library-read")
        token_info = self.retrieve_recent_token()
        print(token_info)
        if not token_info:
            auth_url = sp_oauth.get_authorize_url()
        print(auth_url)
        response = input('Paste the above link into your browser, then paste the redirect url here: ')

        code = sp_oauth.parse_response_code(response)
        token_info = sp_oauth.get_access_token(code)

        token = token_info['access_token']
        self.cache_token("tokens", token)
        return token
    def search(self, artist=None, track=None):
        result = self.spotipyobj.search(q="artist: {} track:{}".format(artist, track))
        if(len(result) == 0):
            return {}
        return result['tracks']['items'][0]
    def createNew(self, name, description="This is made from a bot I made!!!!!"):
        scope = 'playlist-modify-private playlist-modify-public playlist-read-private'
        token = util.prompt_for_user_token(username=self.username, scope='playlist-modify playlist-modify-private', client_id=self.client, client_secret=self.secret)
        url = "https://api.spotify.com/v1/users/%s/playlists" % (self.username)
        headers = {'Accept' : 'application/json', 'Authorization' : token, 'Content-Type' : "application/json"}
        data = "{\"name\":\"%s\",\"public\":true}" % (name)
        data = data.encode('UTF-8')
        r = requests.post(url, headers=headers, data=data)
    def addtoplaylist(self, token, trackIDs, playlist='6EsA2djKdRw4dFxzLeWSEs'):
        # how the hell I was supposed to send the requests -> https://github.com/mileshenrichs/spotify-playlist-generator/blob/master/generate.py
        reqHeader = {'Authorization': 'Bearer {}'.format(token), 'Content-Type': 'application/json'}
        # nice touch with the lambda dude{ette}
        reqBody = {'uris': list(map((lambda songId: 'spotify:track:' + songId), trackIDs))}
        print(reqBody)

        r = requests.post('https://api.spotify.com/v1/playlists/{}/tracks'.format(playlist),
        headers=reqHeader, json=reqBody)
    def addtoplaylistBASH(self, token, trackIDs, playlist='6EsA2djKdRw4dFxzLeWSEs'):
        for element in trackIDs:
            call(["./addPlaylist.sh", playlist, element, token])

    def convert_json_to_set(self, AppleMusicObj):
        musicIDS = set()
        for artist, track in AppleMusicObj.manifest.items():
            if(len(track) > 1):
                for item in track:
                    res = spot.search(artist, item)
                    musicIDS.add(res['id'])
            elif len(track) == 1:
                res = spot.search(artist, track)
                musicIDS.add(res['id'])
        return musicIDS
    def convert_json_data_to_id_manifest(self, musicSet, path):
        with open(path, "w+") as filePointer:
            for element in musicSet:
                filePointer.write(element)
                filePointer.write("\n")
        filePointer.close()
    def cache_token(self, path, token):
        with open(path, 'w+') as file:
            file.write(token)

apple = AppleMusic.AppleMusicPlayist("https://itunes.apple.com/us/playlist/rock-hits-2007/pl.3af683127d6b4f21bd5a2f397b044f3b")
spot = SpotifyPlaylist()
musicset = spot.convert_json_to_set(apple)
spot.getAccessToken()
spot.addtoplaylistBASH(spot.retrieve_recent_token(), musicset)
