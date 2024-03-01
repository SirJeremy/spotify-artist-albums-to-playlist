from pydantic import BaseModel, Field
from dotenv import dotenv_values

class Config(BaseModel):
    LOOP_PROGRAM:bool = Field(default=True)
    SPOTIFY_CLIENT_SCOPES:str = Field(default="user-library-read playlist-read-private playlist-modify-private playlist-modify-public")
    INCLUDE_GROUPS:str = Field(default="album,single,appears_on,compilation,")
    NEWEST_ALBUM_FIRST:bool = Field(default=False)
    PRESERVE_TRACK_ORDER:bool = Field(default=True)

def load_config() -> Config:
    config_overrides = dotenv_values("config.txt")
    config = Config.model_validate(config_overrides)
    return config
