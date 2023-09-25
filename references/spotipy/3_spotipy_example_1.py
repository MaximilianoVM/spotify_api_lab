import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

kanye_uri = 'https://open.spotify.com/artist/5K4W6rqBFWDnAN6FQUkS6x?si=yWi9lBLjTk2mugnsxTzvQg'

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id="ee8117f8e4ef406eb79aee4569842953", 
                                                                              client_secret="179d7b629d7e41c1bc138aa4274bac20"))

results = spotify.artist_albums(kanye_uri, album_type='album')



albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])
    

    