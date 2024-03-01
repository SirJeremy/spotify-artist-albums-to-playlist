import spotipy
from models import Album, Playlist, Track

def get_all_artist_tracks(client:spotipy.Spotify, artist_id:str, include_groups:str,
                          newest_album_first:bool=False, preserve_track_order:bool=True) -> list[Track]:
    """
    - newest_album_first : Will change the order in which tracks of albums are returned to newest first.
    - preserve_track_order : Will preserver the order of tracks. Only noticeable if albums are ordered newest first.

    If newest_album_first and not preserve_track_order, then tracks will be ordered newsest first.
    """

    artist_tracks: list[Track] = []
    artist_albums = get_all_artist_albums(client, artist_id, include_groups)
    artist_albums.sort(key=lambda x: x.release_date, reverse=newest_album_first)
    
    for album in artist_albums:
        album.tracks.extend(get_tracks_from_album(client, album.id, artist_id))
        if newest_album_first and not preserve_track_order:
            album.tracks.reverse()
        artist_tracks.extend(album.tracks)

    return artist_tracks

def get_all_artist_albums(client:spotipy.Spotify, artist_id:str, include_groups:str) -> list[Album]:
    artist_albums:list[Album] = []
    offset = 0
    limit = 50

    while True:
        results = client.artist_albums(artist_id=artist_id, album_type=include_groups, offset=offset, limit=limit)
        if len(results['items']) == 0:
            return artist_albums
        offset += limit
        for album in results['items']:
            artist_albums.append(Album.model_validate(album))
        if len(results['items']) < limit:
            return artist_albums

def get_all_playlists(client:spotipy.Spotify) -> list[Playlist]:
    playlists:list[Playlist] = []
    offset = 0
    limit = 50

    while True:
        results = client.current_user_playlists(offset=offset, limit=limit)
        if len(results['items']) == 0:
            return playlists
        offset += limit
        for playlist in results['items']:
            playlists.append(Playlist.model_validate(playlist))
        if len(results['items']) < limit:
            return playlists

def get_tracks_from_album(client:spotipy.Spotify, album_id:str, artist_id:str) -> list[Track]:
    tracks:list[Track] = []
    offest = 0
    limit = 50

    while True:
        results = client.album_tracks(album_id=album_id, limit=limit, offset=offest)
        if len(results['items']) == 0:
            return tracks
        offest += limit
        for track in results['items']:
            t = Track.model_validate(track)
            if t.has_artist(artist_id):
                tracks.append(t)
        if len(results['items']) < limit:
            return tracks