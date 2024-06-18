import os
from mutagen.mp3 import MP3
from .util import MizikaCantReadFileError

class Song:
    def __init__(self, path:str):
        # if os.path.isdir():
        #     raise MizikaCantReadFileError(f"This path belongs to a directory: {path}")
        # if os.path.splitext()[1] == ".mp3":
        #     raise MizikaCantReadFileError(f"I can read only mp3 file: {path}")
        # try:
        #     self.length:float = MP3(path).info.length
        # except Exception as e:
        #     raise MizikaCantReadFileError(e)

        try:
            self.__length:float = MP3(path).info.length
        except Exception as e:
            raise MizikaCantReadFileError(e)

        self.__path:str = path
        self.__name:str = os.path.basename(path) # RAM'im bol

    def get_name(self) -> str:
        return self.__name 

    def get_length(self) -> float:
        return self.__length

    def get_path(self) -> str:
        return self.__path

