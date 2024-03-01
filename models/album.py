from pydantic import BaseModel, Field
from models.track import Track

class Album (BaseModel):
    name:str
    id:str
    album_type:str
    album_group:str
    release_date:str
    spotify_uri:str = Field(alias='uri')
    tracks:list[Track] = Field(default=[]) # filled externally
    
    def __str__(self) -> str:
        return f"{self.name} ({self.release_date})"
    
    # Example Source Data
    # {
    #     'album_group': 'album',
    #     'album_type': 'album',
    #     'artists': [{...}],
    #     'available_markets': ['AR', 'AU', 'AT', 'BE', 'BO', 'BR', 'BG', 'CA', 'CL', ...],
    #     'external_urls': {'spotify': 'https://open.spotify.com/album/04ONmNNxR2jUOfDuFmbSBO'},
    #     'href': 'https://api.spotify.com/v1/albums/04ONmNNxR2jUOfDuFmbSBO',
    #     'id': '04ONmNNxR2jUOfDuFmbSBO',
    #     'images': [{...}, {...}, {...}],
    #     'name': 'Bloodletting & Quail Eggs',
    #     'release_date': '2023-02-20',
    #     'release_date_precision': 'day',
    #     'total_tracks': 13,
    #     'type': 'album',
    #     'uri': 'spotify:album:04ONmNNxR2jUOfDuFmbSBO'
    # }