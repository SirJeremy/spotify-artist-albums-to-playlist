import spotipy
from models import Playlist, Track

def prompt_for_playlist(client:spotipy.Spotify, user_id:str) -> Playlist:
    choice_new = "n"
    choice_search = "s"
    choice_link = "l"

    playlist:Playlist = None
    while True:
        print("Now select which playlist to add the songs to. It must be one that you own.")
        uin = input("Would you like to create a new one, search for existing, or provie a direct link to existing? "
                    + f"({choice_new} for new, {choice_search} for search, or {choice_link} for link): ")
        if uin == choice_new:
            playlist = create_playlist(client, user_id)
        elif uin == choice_search:
            playlist = search_for_playlist(client, [user_id])
        elif uin == choice_link:
            playlist = get_playlist_from_link(client)
        if playlist is not None:
            return playlist
        
def add_tracks_to_playlist(client:spotipy.Spotify, playlist:Playlist, tracks:list[Track]):
    if len(tracks) == 0:
        return
    
    batch_size = 100 # there is a limit of 100 per request
    batch = 1

    while True:
        uris:list[str] = []
        i = 0

        # range(start of batch range to the end of tracks or end of batch, whichever happens first)
        for i in range(batch_size * (batch-1), min(len(tracks), batch_size * batch)):
            uris.append(tracks[i].spotify_uri)

        client.playlist_add_items(playlist_id=playlist.id, items=uris)

        # if all tracks added, stop, else next batch
        if i+1 == len(tracks):
            return
        batch += 1

def create_playlist(client:spotipy.Spotify, user_id:str) -> Playlist:
    choice_quit = "!q"

    name = ""
    while True:
        uin = input(f"Enter playlist name ({choice_quit} to quit): ")

        if uin == choice_quit:
            return None
        
        uin = uin.strip()
        if uin != "":
            name = uin
            break
        print("Invalid name.")
        
    print(f"Creating playlist '{name}'")
    raw_playlist = client.user_playlist_create(user=user_id, name=name, public=False)
    raw_playlist['owner']['display_name'] = user_id # api change broke code, this is workaround. value unimportant
    return Playlist.model_validate(raw_playlist)

def search_for_playlist(client:spotipy.Spotify, owner_ids:list[str]) -> Playlist|None:
    choice_quit = "!q"

    while True:
        # prompt for search
        uin = input(f"Enter the name of one of your playlists to search ({choice_quit} to quit): ")
        if uin == choice_quit:
            return None
        search = uin

        # search; if search valid: refine search, else: reprompt
        limit = 10
        (offset, results) = _find_playlists_of_owner(client=client, playlist_name=search, limit=limit, owner_ids=owner_ids)
        if len(results) == 0:
            print("No playlists found.")
            continue

        # print results
        for idx, r in enumerate(results):
            print(f"{(idx+1):>2d} {r.name} - {r.owner_name}")
        
        # make selection
        selection = _select_playlist_from_search(client, search, owner_ids, offset, results)

        # if selection quit, new search
        if selection == None:
            continue
        # if selection made, return result
        elif selection >= 0:
            return results[selection]

def get_playlist_from_link(client:spotipy.Spotify) -> Playlist|None:
    playlist:Playlist = None

    choice_quit = "!q"
    choice_confirm = "y"

    while True:
        uin = input(f"Please paste playlist id, uri, or link ({choice_quit} to quit): ")
        if uin == choice_quit:
            break
        try:
            playlist = Playlist.model_validate(client.playlist(uin))
        except Exception:
            playlist = None
            print("No playlist found.")   
            continue
        uin = input(f'Playlist "{playlist.name}" found. Confirm? ({choice_confirm} or anything else for no): ')
        if uin == choice_confirm:
            break
        else:
            playlist = None

    return playlist

def _select_playlist_from_search(client:spotipy.Spotify, search:str, owner_ids:list[str], offset:int, results:list[Playlist]) -> int|None:
    choice_print_all = "p"
    choice_print_recent = "r"
    choice_more = "m"
    choice_search = "s"

    last_results_idx = 0

    while True:
        print(f"({choice_print_all} to print all results, {choice_print_recent} to reprint most recent results, "
                + f"{choice_more} for more results, {choice_search} go back to search")
        uin = input("Enter number of playlist to confirm: ")
        # go back to search
        if uin == choice_search:
            return None
        # print all results
        elif uin == choice_print_all:
            for idx, r in enumerate(results):
                print(f"{(idx+1):>2d} {r.name} - {r.owner_name}")
            continue
        # reprint results
        elif uin == choice_print_recent:
            for i in range(last_results_idx, len(results)):
                print(f"{(i+1):>2d} {results[i].name} - {results[i].owner_name}")
            continue
        # get more results
        elif uin == choice_more:
            previous_length = len(results)
            limit = 10
            (offset, new_results) = _find_playlists_of_owner(client=client, playlist_name=search, limit=limit,
                                                            offset=offset, owner_ids=owner_ids)
            if len(new_results) == 0:
                print("No more results.")
                continue
            results.extend(new_results)
            last_results_idx = previous_length
            for i in range(last_results_idx, len(results)):
                print(f"{(i+1):>2d} {results[i].name} - {results[i].owner_name}")
            continue
        # parse for selection
        else:
            selection = 0
            try:
                selection = int(uin)-1
            except ValueError:
                print("Invalid selection.")
                continue
            if selection < 0 or selection >= len(results):
                print("Invalid selection.")
                continue
            return selection

def _find_playlists_of_owner(client:spotipy.Spotify, playlist_name:str, owner_ids:list[str],
                             limit:int, offset:int=0, max_attempts:int=10) -> tuple[int, list[Playlist]]:
        """Seraches for playlists and excludes those that do not have an owner in owner_ids.
        Will do additional searches if no valid results are found.
        If no valid results found after all attempts, then it assumed taht no valid result exists.
        
        Retuns a tuple of (offset:int, playlists:list[Playlist])."""

        attempt = 0
        playlists:list[Playlist] = []

        while attempt < max_attempts:
            results = client.search(q=playlist_name, limit=limit, offset=offset, type="playlist")['playlists']['items']

            offset += limit
            attempt += 1

            for r in results:
                playlist = Playlist.model_validate(r)
                if playlist.has_owner(owner_ids):
                    playlists.append(playlist)

            if len(playlists) > 0:
                break
            
        return offset,playlists