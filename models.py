from pydantic import BaseModel


class SongData(BaseModel): 
    lyric: str
    genre: str
    tags: list[str]