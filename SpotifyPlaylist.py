#!/usr/bin/env python3.5

# big thanks to this github repo https://github.com/mileshenrichs/spotify-playlist-generator/blob/master/generate.py

import sqlite3
import requests
from  bs4 import BeautifulSoup
import urllib.parse
import datetime
import SQLite

class SpotifyPlaylist():
    def __init__(self, name=None, url=None):
        self.name = name
        self.url = url
    def getAccessToken(self, database, connection):
        database.execute("SELECT value FROM tokens WHERE token_type = 'encoded_basic_token'")
        basicToken = database.fetchone()[0]
        database.execute("SELECT value FROM tokens WHERE token_type = 'refresh_token'")
        refreshToken = database.fetchone()[0]
        reqHeader = {'Authorization': 'Basic {}'.format(basicToken)}
        reqBody = {'grant_type': 'refresh_token', 'refresh_token': refreshToken}
        r = requests.post('https://accounts.spotify.com/api/token', headers=reqHeader, data=reqBody)
        resJson = r.json()

        newToken = resJson['access_token']
        # update token in db
        database.execute("UPDATE tokens SET value = ? WHERE token_type = 'access_token'", (newToken,))
        connection.commit()
        return newToken

    def genDatabase(self, token=None):
        # learning how to operate on SQLITE Files -> https://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html
        sqlite_file = 'script.sqlite'    # name of the sqlite database file
        table_name1 = 'tokens'  # name of the table to be created
        table_name2 = 'jared'
        new_field = 'token_type' # name of the column
        field_type_one = 'encoded_basic_token'  # column data type
        field_type_two = 'access_token'
        field_type_three = 'refresh_token'
        id_column = 'my_1st_column'
        column_name = 'my_2nd_column'

        # Connecting to the database file
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()

        # Creating a new SQLite table with 1 column
        c.execute('CREATE TABLE {tn} ({nf} {ft})'\
                .format(tn=table_name2, nf=new_field, ft=field_type_one))

        # Creating a second table with 1 column and set it as PRIMARY KEY
        # note that PRIMARY KEY column must consist of unique values!
        # c.execute('CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY)'.format(tn=table_name1, nf=new_field, ft=field_type_one))
        c.execute("INSERT INTO {tn} ({idf}, {cn}) VALUES (123456, 'test')".format(tn=table_name2, idf=id_column, cn=column_name))
        # Committing changes and closing the connection to the database file
        conn.commit()
        conn.close()

a = SpotifyPlaylist()
data = SQLite.database("hello.sqlite")
# a.genDatabase()
