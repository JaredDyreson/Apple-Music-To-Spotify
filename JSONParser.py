#!/usr/bin/env python3.5
import json
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
