from lib2to3.pgen2 import token
from operator import is_
from bs4 import ResultSet
from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import pandas as pd

app = Flask(__name__)

app.secret_key = "AIOa324ljkhHJK"
app.config['SESSION_COOKIE_NAME'] = 'Cookie'
TOKEN_INFO = "token_info"

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    print(auth_url)
    return redirect(auth_url)

@app.route('/authorize')
def authorize():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('getTracks', _external=True))

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')        

@app.route('/getTracks')
def getTracks():
    session[TOKEN_INFO], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect('/')

    sp = spotipy.Spotify(auth=session.get(TOKEN_INFO).get('access_token'))

    results = []
    tracks = []
    n = 0
    while True:
        offset = n * 50
        n += 1
        items =  sp.current_user_saved_tracks(limit=50, offset=offset)['items']
        # playlists = sp.current_user_playlists(limit=50, offset=0)
        # for playlist in enumerate(playlists):
        #     print(playlist)
        #     items = sp.playlist_tracks(playlist[0], fields = None, limit=100, offset=0, market=None)
        #     tracks += [items]

        for idx, item in enumerate(items):
            track = item['track']
            val = track['name'] + '-' + track['artists'][0]['name']
            results += [val]
        if len(items) < 50:
            break

    df = pd.DataFrame(results, columns=['song_names'])
    df.to_csv('songs.csv', index=False)
    return 'done'

def get_token():
    token_valid = False
    token_info = session.get(TOKEN_INFO, {})
    if not (session.get(TOKEN_INFO, False)):
        token_valid = False
        return token_info, token_valid

    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60

    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(session.get(TOKEN_INFO).get('refresh_token'))

    token_valid = True
    return token_info, token_valid


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id = "7ae897e37dd24ed48ab052f0e1a633d8",
        client_secret = "f2357d9a4a1b4ebaa0c8c921695142a9", 
        redirect_uri = url_for('authorize', _external=True),
        scope="user-library-read"
    )