#!/usr/bin/env bash

# $1 == playlistID
# $2 == trackID
# $3 == keyID

curl -X "POST" "https://api.spotify.com/v1/playlists/"$1"/tracks?uris=spotify%3Atrack%3A"$2"" -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer $3" -d "Content-Length: 0"
