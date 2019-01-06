#!/usr/bin/env python3.5
import os
import sys
from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
import json


class urlResponse():
    def __init__(self, url, r=None):
        self.url = "https://google.com"
    # @staticmethod
    def is_good_response(self, response):
        content = response.headers['Content-Type'].lower()
        return (response.status_code == 200
                and content is not None
                and content.find('html') > -1)
    # @staticmethod
    def getUrl(self, url):
        try:
            with closing(get(url, stream=True)) as response:
                if(self.is_good_response(response)):
                    return response.content
                else:
                    return None
        except RequestException as e:
            print("Error, shrug")

class AppleMusicPlayist():
    # cached feature to use the json file created so you don't have to keep sending requests to the site
    def __init__(self, url=None, cachedJSON=None):
        self.sendAppleRequest = True
        self.url = url
        self.cachedJSON = cachedJSON

        # if we have something passed (filepath), we need to check if it is accessible
        try:
            if cachedJSON != None:
                fh = open(cachedJSON, 'r')
                self.sendAppleRequest = False
                fh.close()
        except FileNotFoundError or cachedJSON == None:
            # if not , we need to specify a new location but also send it over to send a request to Apple
            self.cachedJSON = self.title + ".json"
        self.loadjson(cachedJSON)

        self.manifest = {}

        if self.sendAppleRequest:
            self.bot = urlResponse(self.url)
            self.html = BeautifulSoup(self.bot.getUrl(self.url), 'html.parser')
            self.manifest = dict(zip(self.artists(), self.songs()))
        else:
            print("loading json")
            self.loadjson(cachedJSON)
            print(self.manifest)

    # functions that do the work
    def artists(self):
        if self.sendAppleRequest:
            raw_artists = self.html.find_all("a", {"class": "table__row__link table__row__link--secondary"})
            return [artist.text for artist in raw_artists]
        else:
            return []
    def songs(self):
        if self.sendAppleRequest:
            raw_songs = self.html.find_all("a", {"class": "tracklist-item__text__link targeted-link targeted-link--no-monochrome-underline"})
            parsed_songs = []
            for i in raw_songs:
                song = str(i.find("span", {"class": "we-truncate we-truncate--single-line ember-view tracklist-item__text__headline targeted-link__target"}).text)
                song = " ".join(song.split())
                parsed_songs.append(song)
            return parsed_songs
        return []
    def title(self):
        if self.sendAppleRequest:
            return(self.html.find("h1", {"class": "product-header__title"}).text)
        return "placeholder string"
    def loadjson(self, path):
        jsonfile = open(path)
        jsonstr = jsonfile.read()
        self.manifest = json.loads(jsonstr)
    # "getter methods", more of an abstraction layer
    def songCount(self):
        return len(self.songs())
    def artistCount(self):
        return len(set(self.artists()))


def unit():
    playlist = AppleMusicPlayist("https://itunes.apple.com/us/playlist/rock-hits-2007/pl.3af683127d6b4f21bd5a2f397b044f3b")
    print("Title: ", playlist.title())
    song_manifest = playlist.songs()
    artist_manifest = playlist.artists()
    print("Songs: "+"\n")
    for song in song_manifest:
        print(song)
    print("\n")
    print("Artists: "+"\n")
    for artist in artist_manifest:
        print(artist)
    print("Number of songs: ", playlist.songCount())
    print("Number of artists: ", playlist.artistCount())
def jsontest():
    playlist = AppleMusicPlayist(url=None, cachedJSON="result.json")
    print(playlist.manifest)
    song_manifest = playlist.songs()
    artist_manifest = playlist.artists()
    print("Songs: "+"\n")
    for song in song_manifest:
        print(song)
    print("\n")
    print("Artists: "+"\n")
    for artist in artist_manifest:
        print(artist)
    print("Number of songs: ", playlist.songCount())
    print("Number of artists: ", playlist.artistCount())
unit()
jsontest()
