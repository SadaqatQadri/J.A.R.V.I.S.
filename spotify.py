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

def pause():
    sp.pause_playback()
    print("Paused, sir.")

def resume():
    sp.start_playback()
    print("Resumed, sir.")

def skip():
    sp.next_track()
    print("Skipped to the next track, sir.")

def previous():
    sp.previous_track()
    print("Went back to the previous track, sir.")

def volume(level):
    sp.volume(level)
    print("Volume set to " + str(level) + ", sir.")

def current_track():
    track = sp.current_user_playing_track()
    if track:
        name = track["item"]["name"]
        artist = track["item"]["artists"][0]["name"]
        print("Currently playing: " + name + " by " + artist)
    else:
        print("Nothing is currently playing, sir.")

while True:
        command = input ("Command, sir? (play/pause/resume/skip/back/volume/current/quit): ")

        if command == "play":
            song = input("Which song, sir? ")
            play_song(song)
        elif command == "pause":
            pause()
        elif command == "resume":
            resume()
        elif command == "skip":
            skip()
        elif command == "back":
            previous()
        elif command == "volume":
            level = int(input("Volume level (0-100):"))
            volume(level)
        elif command == "current":
            current_track()
        elif command == "quit":
            print("Goodbye, sir.")
            break
         