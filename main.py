import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
from models import Playlist, Artist, Track
from config import Config, load_config

from logic.artists import prompt_for_artist
from logic.tracks import get_all_artist_tracks
from logic.playlists import prompt_for_playlist, add_tracks_to_playlist

def main():
    config:Config = load_config()

    print("Spotify Artist Albums To Playlist")
    print("Need access to user id, playlists, and permission to edit playlists. Accept permissions to continue.")
    client = get_client(config.SPOTIFY_CLIENT_SCOPES)
    user_id = get_current_user_id(client)

    artist:Artist = prompt_for_artist(client)

    artist_tracks:list[Track] = get_all_artist_tracks(
        client,
        artist.id,
        config.INCLUDE_GROUPS,
        config.NEWEST_ALBUM_FIRST,
        config.PRESERVE_TRACK_ORDER
    )

    print(f'{len(artist_tracks)} tracks with artists "{artist.name}" found.')

    prompt_print_tracks(artist_tracks)

    playlist:Playlist = prompt_for_playlist(client, user_id)

    if prompt_confirm_addition(playlist, artist_tracks):
        print(f"Adding songs...")
        add_tracks_to_playlist(client, playlist, artist_tracks)
        print(f"Done!")
    else:
        print("Aborting.")

# region functions
        
def get_client(scope:str) -> spotipy.Spotify:
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.environ['CLIENT_ID'],
        client_secret=os.environ['CLIENT_SECRET'],
        redirect_uri=os.environ['REDIRECT_URI'],
        scope=scope
    ))

def get_current_user_id(client:spotipy.Spotify) -> str:
    return client.current_user()['id']

def prompt_print_tracks(tracks:list[Track]):
    choice_confirm = "y"

    if input(f"Display songs? ({choice_confirm} or anthing else for no): ") == choice_confirm:
        for idx, track in enumerate(tracks):
            print(f"{(idx+1):>3d} {track.name} - {track.get_artists_str()}")

def prompt_confirm_addition(playlist:Playlist, artist_tracks:list[Track]) -> bool:
    choice_confirm = "y"
    choice_deny = "n"

    while True:
        uin = input(f"Playlist '{playlist}' selected. Confirm adding {len(artist_tracks)} songs? ({choice_confirm} or {choice_deny}): ")
        if uin == choice_confirm:
            return True
        elif uin == choice_deny:
            return False
        else:
            print("Invalid input.")    

# endregion functions
            
if __name__ == "__main__":
    load_dotenv()
    try:
        main()
    except Exception as e:
        print("Unexpected error occured")
        print(e)