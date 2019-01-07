#!/usr/bin/env python3.5
import AppleMusic
def unit():
    playlist = AppleMusic.AppleMusicPlayist("https://itunes.apple.com/us/playlist/rock-hits-2007/pl.3af683127d6b4f21bd5a2f397b044f3b")
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
    playlist.dumpjson(playlist.title())
def jsontest():
    playlist = AppleMusic.AppleMusicPlayist(url=None, cachedJSON="Rock Hits: 2007")
    print(playlist.manifest)
    print(playlist.title())

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
