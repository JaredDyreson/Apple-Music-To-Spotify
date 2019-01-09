#!/usr/bin/env python3.5
import os
import sys
from bs4 import BeautifulSoup
import json
from collections import defaultdict
# my classes I pieced together
import FileHandler
import URLResponse as ur

class AppleMusicPlayist():
    # cached feature to use the json file created so you don't have to keep sending requests to the site
    def __init__(self, url=None, cachedJSON=None):
        self.sendAppleRequest = True
        self.url = url
        self.cachedJSON = cachedJSON
        self.filehandler = FileHandler.FileHandler(cachedJSON)
        self.manifest = {}

        if self.sendAppleRequest and self.url != None:
            self.bot = ur.urlResponse(self.url)
            self.html = BeautifulSoup(self.bot.getUrl(self.url), 'html.parser')
            t = defaultdict(list)

            for c, i in zip(self.artists(), self.songs()):
                t[c].append(i)
            self.manifest = t
        else:
            self.loadjson(cachedJSON)

        # if we have something passed (filepath), we need to check if it is accessible
        if(self.filehandler.is_open()):
            sendAppleRequest = False
            self.loadjson(cachedJSON)
        else:
            self.cachedJSON = self.title() + ".json"
        # self.titular = self.title()
    # functions that do the work
    def artists(self):
        if self.sendAppleRequest and self.url != None:
            raw_artists = self.html.find_all("a", {"class": "table__row__link table__row__link--secondary"})
            return [artist.text for artist in raw_artists]
        return [a for a in self.manifest.keys()]
    def songs(self):
        if self.sendAppleRequest and self.url != None:
            raw_songs = self.html.find_all("a", {"class": "tracklist-item__text__link targeted-link targeted-link--no-monochrome-underline"})
            parsed_songs = []
            for i in raw_songs:
                song = str(i.find("span", {"class": "we-truncate we-truncate--single-line ember-view tracklist-item__text__headline targeted-link__target"}).text)
                song = " ".join(song.split())
                parsed_songs.append(song)
            return parsed_songs
        return [item for sublist in self.manifest.values() for item in sublist] # https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists
    def title(self):
        if self.sendAppleRequest and self.url != None:
            return(self.html.find("h1", {"class": "product-header__title"}).text)
        return "placeholder string"
    def loadjson(self, path):
        jsonfile = open(path)
        jsonstr = jsonfile.read()
        self.manifest = json.loads(jsonstr)
    def dumpjson(self, path):
        with open(path, "w+") as file:
            json.dump(self.manifest, file, indent=4, sort_keys=True)
    # "getter methods", more of an abstraction layer
    def songCount(self):
        return len(self.songs())
    def artistCount(self):
        return len(set(self.artists()))
