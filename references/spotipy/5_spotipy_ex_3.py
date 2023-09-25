import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id="ee8117f8e4ef406eb79aee4569842953", 
                                                                              client_secret="179d7b629d7e41c1bc138aa4274bac20"))

if len(sys.argv) > 1:
    name = ' '.join(sys.argv[1:])
else:
    name = 'Radiohead'

results = spotify.search(q='artist:' + name, type='artist')
items = results['artists']['items']
if len(items) > 0:
    artist = items[0]
print(artist['name'], artist['images'][0]['url'])