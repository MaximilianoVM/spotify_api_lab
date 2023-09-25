import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth

from flask import Flask, request, url_for, session, redirect, render_template

app = Flask(__name__)

app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
app.secret_key = 'DELETED'

TOKEN_INFO = 'token_info'

@app.route('/')
def index():
    return render_template('index.html')
### ====================================================================================================

#////-----INICIA SESION EN SPOTIFY-----////
@app.route('/login_spotify')
def login():
    auth_url = create_spotify_oauth().get_authorize_url() # external authorize url (se define abajo)
    return redirect(auth_url) # redirecting user to that external url

#////-----REDIRECT-----////
@app.route('/redirect') #no se donde se usa, pero si la quitas da error, creo que la busca el mismo navegador
def redirect_page():
    session.clear()
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info
    #return redirect(url_for('save_discover_weekly', _external = True)) ## despues del redirect te lleva a save_discover_weekly
    return redirect(url_for('select_playlist', _external = True))

#////-----BOTON PARA CLONAR-----////
#@app.route('/click_to_function')
#def click_to_function():
#    return render_template('click_to_function.html')

#////-----SELECT PLAYLIST-----////
@app.route('/select_playlist')
def select_playlist():
    try:
        token_info = get_token() # Try to get token
    except:
        print('User not logged in') # Log in 
        return redirect('/')
    #return("OAUTH SUCCESSFUL")

    sp = spotipy.Spotify(auth=token_info['access_token']) #funcion para sacar chotas de spotify
    current_playlists = sp.current_user_playlists()['items'] #conjunto de playlists

    return render_template('select_pl.html', playlists=current_playlists)

#////-----CLONE SELECTED PLAYLIST-----////
@app.route('/clone_playlist', methods=['POST'])
def clone_playlist():
    to_clone_playlist_id = request.form.get('playlist_id') #nos la traemos de la forma(en select_pl.html)
    cloned_playlist_name = request.form.get('playlist_name') #nos la traemos de la forma(en select_pl.html)


    #----->>>>>
    # Perform the playlist cloning logic here using the selected_playlist_id

    #copied and adapted from save_discover_weekly
    try:
        token_info = get_token() #try to get token
    except:
        print('user not logged in') #log in 
        return redirect('/')
    
    #return("OAUTH SUCCESSFUL")

    sp = spotipy.Spotify(auth=token_info['access_token'])   #SPOTIFY function
    user_id = sp.current_user()['id']                       #get USER from SPOTIFY function
    cloned_playlist_id = None                         #gonna be the id of the cloned pl

    current_playlists = sp.current_user_playlists()['items'] #Conjunto de playlists
    
    #recorremos todas las pl que ya tenemos
    for playlist in current_playlists:
        #Vemos si ya esta clonada
        #if(playlist['name'] == 'CLONED'):
        if(playlist['name'] == cloned_playlist_name):
            print("{} IS IN PLAYLISTS || ID:".format(cloned_playlist_name), playlist['id'])
            cloned_playlist_id = playlist['id']
            print("====>>>>{}_id:".format(cloned_playlist_name), cloned_playlist_id)
            
    #si no existe la clonada, la hacemos
    #CREAMOS PLAYLIST
    if not cloned_playlist_id:    
        new_playlist = sp.user_playlist_create(user_id, cloned_playlist_name, True)
        cloned_playlist_id = new_playlist['id']
    
    to_clone_playlist = sp.playlist_items(to_clone_playlist_id) #le sacamos el id a la pl a clonar
    song_uris = []
    
    for song in to_clone_playlist['items']:   #recorremos las canciones de la pl original
        song_uri = song['track']['uri']     
        song_uris.append(song_uri)
    
    #para crear la nueva pl pide: user_id, id de la pl objetivo, song_uris
    sp.user_playlist_add_tracks(user_id, cloned_playlist_id, song_uris, None)
    
    return('SUCCESS!!!!')

### ====================================================================================================

@app.route('/run_function', methods=['POST'])
def run_function():
    # Your function logic here
    result = "Function executed!"  # Replace with the result of your function
    return render_template('result.html', result=result)

@app.route('/prueba', methods=['POST'])
def prueba():
    return " <h1> JAJAJAJAJAJ </h1> "

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
        client_id='DELETED', 
        client_secret='DELETED', 
        redirect_uri= url_for('redirect_page', _external=True), 
        scope= 'user-library-read playlist-modify-public playlist-modify-private'
        )
  

if __name__ == '__main__':
    app.run(debug=True)
