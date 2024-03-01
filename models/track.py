from pydantic import BaseModel, Field
from models.artist import Artist

class Track (BaseModel):
    name:str
    id:str
    spotify_uri:str = Field(alias='uri')
    artists:list[Artist]

    def get_artists_str(self) -> str:
        artists_names:list[str] = []
        for a in self.artists:
            artists_names.append(a.name)
        return ", ".join(artists_names)
    
    def has_artist(self, artist_id:str) -> bool:
        for artist in self.artists:
            if artist.id == artist_id:
                return True
        return False
    
    def __str__(self):
        return f"{self.name} by {self.artists[0].name}"
    
# Example Source Data
# {
#     'artists': [{   
#         # Same as artist model
#         'external_urls': {...}, 'href': 'https://api.spotify.com/v1/artists/3Sq3ARGLbpAbK1rQ00v6NR',
#         'id': '3Sq3ARGLbpAbK1rQ00v6NR',
#         'name': 'Don Yellow',
#         'type': 'artist',
#         'uri':
#         'spotify:artist:3Sq3ARGLbpAbK1rQ00v6NR'
#     }],
#     'disc_number': 1.0,
#     'duration_ms': 172199.0,
#     'explicit': True,
#     'external_urls': {'spotify': 'https://open.spotify.com/track/6jcPkSaHYXjmYb6m7KyS1C'},
#     'href': 'https://api.spotify.com/v1/tracks/6jcPkSaHYXjmYb6m7KyS1C',
#     'id': '6jcPkSaHYXjmYb6m7KyS1C',
#     'is_local': False,
#     'is_playable': True,
#     'name': 'Watch Me Groove',
#     'preview_url': 'https://p.scdn.co/mp3-preview/2f979dad3a1ffe9850eb683e1f9e2447892e7fa1?cid=b5894fd7d32a459494d5fe73b2939b24',
#     'track_number': 1.0,
#     'type': 'track',
#     'uri': 'spotify:track:6jcPkSaHYXjmYb6m7KyS1C'
# }