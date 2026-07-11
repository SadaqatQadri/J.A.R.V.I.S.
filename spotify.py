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
        return "Sorry sir, I couldn't find that song."

    track = tracks[0]
    track_uri = track['uri']
    track_name = track['name']
    artist_name = track['artists'][0]['name']

    sp.start_playback(uris=[track_uri])
    return "Now playing: " + track_name + " by " + artist_name

def play_playlist(playlist_name):
    results = sp.search(q=playlist_name, limit=1, type="playlist")
    playlists = results["playlists"]["items"]

    if not playlists:
        return "Sorry sir, I couldn't find that playlist."

    playlist = playlists[0]
    playlist_uri = playlist["uri"]
    playlist_name_found = playlist["name"]

    sp.start_playback(context_uri=playlist_uri)
    return "Now playing: " + playlist_name_found

def pause():
    sp.pause_playback()
    return "Paused, sir."

def resume():
    sp.start_playback()
    return "Resumed, sir."

def skip():
    sp.next_track()
    return "Skipped to the next track, sir."

def previous():
    sp.previous_track()
    return "Went back to the previous track, sir."

def volume(level):
    sp.volume(level)
    return "Volume set to " + str(level) + ", sir."

def current_track():
    track = sp.current_user_playing_track()
    if track:
        name = track["item"]["name"]
        artist = track["item"]["artists"][0]["name"]
        return "Currently playing: " + name + " by " + artist
    else:
        return "Nothing is currently playing, sir."

if __name__ == "__main__":
    while True:
        command = input("Command, sir? (play/pause/resume/skip/back/volume/current/quit): ")

        if command == "play":
            song = input("Which song, sir? ")
            print(play_song(song))
        elif command == "playlist":
            playlist = input("Which playlist, sir? ")
            print(play_playlist(playlist))
        elif command == "pause":
            print(pause())
        elif command == "resume":
            print(resume())
        elif command == "skip":
            print(skip())
        elif command == "back":
            print(previous())
        elif command == "volume":
            level = int(input("Volume level (0-100):"))
            print(volume(level))
        elif command == "current":
            print(current_track())
        elif command == "quit":
            print("Goodbye, sir.")
            break