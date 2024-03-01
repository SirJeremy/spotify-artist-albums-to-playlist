# spotify-artist-albums-to-playlist

![Preview of program appearance](https://raw.githubusercontent.com/SirJeremy/spotify-artist-albums-to-playlist/master/preview.png)

This project has a solution to a very specific problem. If you ever have wanted to go through an artists entire discography on Spotify, you would need to hunt down every song, manually add them to a playlist, and then order them by year. UI updates make this less of a pain, but only by about 20%.

With this script, all you need to do is select an artist and playlist, and then every song by the artist gets added to the playlist.

To actually do so, this script requires some permissions on your account. It needs permission to read your user info for user ID, and read and write permission to your library to be able to add songs to your playlists. Permissions are stored locally in a cache file.

## Requirements

Python >=3.10 Required

Required packages listed in `requirements.txt`. Either install them manually, or use the common command `pip install -r requirements.txt`.

API access is required. Check the [official documentation](https://developer.spotify.com/documentation/web-api) on how to get an API key. Once you get this you need to add it to a `.env` file in the root folder. Check the `env-template.txt` for an example. You will specifically need a client id, client secret, and redirect URI from the app authorization on the API.

This setup should only need to be done once.