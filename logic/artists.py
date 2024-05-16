import spotipy
from models import Artist

def prompt_for_artist(client:spotipy.Spotify) -> Artist:
    artist:Artist = None

    choice_search = "s"
    choice_link = "l"
    
    while True:
        uin = input(f"First select an artist. Would you like to search or provide direct link? ({choice_search} for search {choice_link} for link): ")
        if uin == choice_search:
            artist = search_for_artist(client)
        elif uin == choice_link:
            artist = get_artists_from_link(client)
        if artist is not None:
            break

    return artist

def search_for_artist(client:spotipy.Spotify) -> Artist:
    choice_quit = "!q"

    while True:
        # prompt for search
        uin = input(f"Enter artist name to search ({choice_quit} to quit): ")
        if uin == choice_quit:
            return None
        search = uin

        # search
        limit = 10
        offset = 0 #must be offset for last valid query for print() purposes
        results = client.search(q=search, limit=limit, offset=offset, type="artist")['artists']['items']

        # reprompt if no results
        if len(results) == 0:
            print("No artists found.")
            continue

        # print results
        for idx, r in enumerate(results):
            print(f"{(idx+1):>2d} {r['name']}")

        # refine search
        selection = _select_artist_from_search(client, search, offset, results)
        
        # if selection None, new search
        if selection == None:
            continue
        # if selection made, return result
        elif selection >= 0:
            return Artist.model_validate(results[selection])

def get_artists_from_link(client:spotipy.Spotify) -> Artist|None:
    artist:Artist = None

    choice_quit = "!q"
    choice_confirm = "y"
    
    while True:
        uin = input(f"Please paste artist id, uri, or link ({choice_quit} to quit): ")
        if uin == choice_quit:
            break
        try:
            artist = Artist.model_validate(client.artist(uin))
        except Exception:
            artist = None
            print("No artist found.")   
            continue
        uin = input(f'Artist "{artist.name}" found. Confirm? ({choice_confirm} or anything else for no): ')
        if uin == choice_confirm:
            break
        else:
            artist = None
    
    return artist

def _select_artist_from_search(client:spotipy.Spotify, search:str, offset:int, results:list[Artist]) -> int|None:
    choice_print_all = "p"
    choice_print_recent = "r"
    choice_more = "m"
    choice_search = "s"

    while True:            
            print(f"({choice_print_all} to print all results, {choice_print_recent} to reprint most recent results, "
                + f"{choice_more} for more results, {choice_search} go back to search")
            uin = input("Enter number of artist to confirm: ")
            # go back to search
            if uin == choice_search:
                return None
            # print all results
            elif uin == choice_print_all:
                for idx, r in enumerate(results):
                    print(f"{(idx+1):>2d} {r['name']}")
                continue
            # reprint results
            elif uin == choice_print_recent:
                for i in range(offset, len(results)):
                    print(f"{(i+1):>2d} {results[i]['name']}")
                continue
            # get more results
            elif uin == choice_more:
                limit = 10
                offset += limit
                results = client.search(q=search, limit=limit, offset=offset, type="artist")['artists']['items']
                if len(results) == 0:
                    print("No more results.")
                    offset -= limit # reset to last valid offeset with results for reprint (r)
                    continue

                for idx, r in enumerate(results):
                    print(f"{(idx+1+offset):>2d} {r['name']}")
                results.extend(results)
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
