from pydantic import BaseModel, Field, AliasPath

class Playlist(BaseModel):
    name:str
    id:str
    description:str
    owner_id:str = Field(alias=AliasPath('owner', 'id'))
    owner_name:str = Field(alias=AliasPath('owner', 'display_name'))
    spoitfy_uri:str = Field(alias='uri')
    
    def has_owner(self, owner_ids:list[str]) -> bool:
        for o in owner_ids:
            if self.owner_id == o:
                return True
        return False
    
    def __str__(self) -> str:
        return self.name

# Example Source Data
# {
#     'collaborative': False,
#     'description': 'Probably the strangest and most unique music I&#x27;ve ever heard',
#     'external_urls': {'spotify': 'https://open.spotify.com/playlist/6P0Js4iQUYoeu4CvqcvSy2'},
#     'href': 'https://api.spotify.com/v1/playlists/6P0Js4iQUYoeu4CvqcvSy2',
#     'id': '6P0Js4iQUYoeu4CvqcvSy2',
#     'images': [{...}],
#     'name': 'Don Yellow',
#     'owner': {
#         'display_name': 'radaa5',
#         'external_urls': {...},
#         'href': 'https://api.spotify.com/v1/users/radaa5',
#         'id': 'radaa5',
#         'type': 'user',
#         'uri': 'spotify:user:radaa5'
#     },
#     'primary_color': None,
#     'public': None,
#     'snapshot_id': 'NDQsZWMxZTU4NzE0ZjE2Y2U5Mzk1ODc0NzJkYTM5MGRjY2JjOTBiZjVmYg==',
#     'tracks': {'href': 'https://api.spotify.com/v1/playlists/6P0Js4iQUYoeu4CvqcvSy2/tracks', 'total': 23},
#     'type': 'playlist',
#     'uri': 'spotify:playlist:6P0Js4iQUYoeu4CvqcvSy2'
# }