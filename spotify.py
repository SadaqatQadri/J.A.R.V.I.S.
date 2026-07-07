import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URL"),
    scope="user-modify-playback-state user-read-playback-state"
))

def play_song(song_name):
    results = sp.search(q=song_name, limit=1, type="track")
    tracks = results['tracks']['items']

    if not tracks:
        print("Sorry sire, I couldn't find that song.")
        return
    
    track = tracks[0]
    track_uri = track['uri']
    track_name = track['name']
    artist_name = track['artists'][0]['name']

    sp.start_playback(uris=[track_uri])
    print("Now playing: " + track_name + " by " + artist_name)

song = input("What would you like to listen to, sir? ")
play_song(song)
