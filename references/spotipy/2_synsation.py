import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth

from flask import Flask, request, url_for, session, redirect

app = Flask(__name__)

app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
app.secret_key = 'alskbfl3fh2kadnj@@ksn'

TOKEN_INFO = 'token_info'

@app.route('/')
def login():
    auth_url = create_spotify_oauth().get_authorize_url() # external authorize url
    return redirect(auth_url) # redirecting user to that external url


#no se donde se usa, pero si la quitas da error, creo que la busca el mismo navegador
@app.route('/redirect')
def redirect_page():
    session.clear()
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('save_discover_weekly', _external = True))


@app.route('/saveDiscoverWeekly')
def save_discover_weekly():
    
    try:
        token_info = get_token() #try to get token
    except:
        print('user not logged in') #log in 
        return redirect('/')
    
    #return("OAUTH SUCCESSFUL")

    sp = spotipy.Spotify(auth=token_info['access_token'])   #SPOTIFY function
    user_id = sp.current_user()['id']                       #get USER from SPOTIFY function
    saved_linger_playlist_id = None                         #we need to get this id later

    current_playlists = sp.current_user_playlists()['items']
    print("CURRENT PLAYLISTS: ", type(current_playlists))
    #for playlist in current_playlists: #[!!!] 
    #    print(playlist['name'])        #[!!!]
    for playlist in current_playlists:
        #para estar seguros, las playlist a tratar deben estar FUERA DE CARPETAS
        if(playlist['name'] == 'LINGER'):
            print("LINGER IS IN PLAYLISTS || ID:", playlist['id'])
            linger_playlist_id = playlist['id']
            print("====>>>>saved_linger_playlist_id:", saved_linger_playlist_id)
            
        if(playlist['name'] == 'Saved LINGER'):
            print("SAVED LINGER IS IN PLAYLISTS || ID:", playlist['id'])
            saved_linger_playlist_id = playlist['id']
            print("====>>>>saved_linger_playlist_id:", saved_linger_playlist_id)
        
    if not linger_playlist_id:          #si no existe la pl original
        return 'LINGER not found'

    if not saved_linger_playlist_id:    #si no existe la duplicada: la hacemos
        new_playlist = sp.user_playlist_create(user_id, 'Saved LINGER', True)
        saved_linger_playlist_id = new_playlist['id']

    linger_playlist = sp.playlist_items(linger_playlist_id) #playlist original
    song_uris = []
    for song in linger_playlist['items']:   #recorremos las canciones de la pl original
        song_uri = song['track']['uri']     
        song_uris.append(song_uri)
    
    #para crear la nueva pl pide: user_id, id de la pl objetivo, song_uris
    sp.user_playlist_add_tracks(user_id, saved_linger_playlist_id, song_uris, None)
    return('SUCCESS!!!!')
        

#======= FUNCIONES ======

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        redirect(url_for('login', _external = False))
        
    now = int(time.time())
    
    is_expired = token_info['expires_at'] - now < 60
    if(is_expired):
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])
        
    return token_info
    

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id='ee8117f8e4ef406eb79aee4569842953', 
        client_secret='179d7b629d7e41c1bc138aa4274bac20', 
        redirect_uri= url_for('redirect_page', _external=True), 
        scope= 'user-library-read playlist-modify-public playlist-modify-private'
        )
    
    
app.run(debug=True)