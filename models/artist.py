from pydantic import BaseModel, Field

class Artist(BaseModel):
    name:str
    id:str
    spotify_uri:str = Field(alias='uri')

    def __str__(self) -> str:
        return self.name

# Example Source Data
# {
#     'external_urls': {'spotify': 'https://open.spotify.com/artist/3Sq3ARGLbpAbK1rQ00v6NR'},
#     'followers': {'href': None, 'total': 1586}, 
#     'genres': [],
#     'href': 'https://api.spotify.com/v1/artists/3Sq3ARGLbpAbK1rQ00v6NR',
#     'id': '3Sq3ARGLbpAbK1rQ00v6NR',
#     'images': [{...}, {...}, {...}],
#     'name': 'Don Yellow',
#     'popularity': 14,
#     'type': 'artist',
#     'uri': 'spotify:artist:3Sq3ARGLbpAbK1rQ00v6NR'
# }