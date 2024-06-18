import os
import json

from .song import Song
from .util import MizikaPlaylistError as PLError
from tools import Event


class Playlist:
    def __init__(self, path:str):
        if os.path.isdir(path):
            raise PLError("Playlist path can't be directory.")
        
        if os.path.splitext(path)[1] == "json":
            raise PLError(f"Playlist file must be '.json' file\n:::{path}:::{os.path.splitext(path)[1]}")
        
        self.__path:str = path
        self.__name:str = os.path.basename(path) 
        self.__length:int = 0
        self.__content:list[Song] = []
        self.content_ch:Event = Event()

    #
    # (G/S)etter
    #

    def get_path(self) -> str: return self.__path
    def get_name(self, wjson=True) -> str: return self.__name if wjson else os.path.splitext(self.__name)[0]
    def get_length(self) -> int: return self.__length
    def get_content(self) -> list[Song]: return self.__content
    def get_path_list(self) -> list[str]: return [song.get_path() for song in self.__content]

    def _set_path(self, new_path:str) -> None:
        '''
            Be carefull
        '''
        self.__path = new_path
        self.__name = os.path.basename(new_path)
    
    
    #
    # Content Methods
    #

    def get_song(self, index:int) -> Song:
        try: return self.__content[index]
        except Exception as e: raise PLError(f"index error. it was {index}")

    def add(self, *songs:Song|str, safe=False, trigger=True) -> None:
        '''
            Add song/songs to playlist
        '''

        if len(songs) == 0: return
        
        if songs[0] is Song:
            for song in songs: 
                self.__content.append(song)
                self.__length += 1
        else:
            for path in songs:
                try: s = Song(path)
                except Exception as e: 
                    if safe: continue
                    raise PLError(e)

                self.__content.append(s)
                self.__length += 1
        
        if trigger: self.content_ch.sync_trigger()

    def pop(self, *indexs:int, trigger=True) -> None:
        _indexs_:list[int] = list(indexs) #
        _indexs_.sort()                   # Index kaymasından dolayı silinecek indisleri bu şekilde ayarlıyoruz
        _indexs_.reverse()                #

        try:            
            for index in _indexs_:
                self.__content.pop(index)
                self.__length -= 1

        except Exception as e: raise PLError(e)

        if trigger: self.content_ch.sync_trigger()

    def clear(self, trigger=True) -> None:
        '''
            All elements
        '''
        self.__content.clear()
        self.__length = 0
        if trigger: self.content_ch.sync_trigger()

    def index(self, song:Song, safe:bool = True) -> int | None:
        try: return self.__content.index(song)
        except Exception as e:
            if safe:
                return None
            raise PLError(e)

    def insert(self, index:int, song:Song, trigger=True) -> None:
        try: self.__content.insert(index, song)
        except Exception as e: raise PLError(e)

        self.__length += 1
        if trigger: self.content_ch.sync_trigger()

    def swap(self, indexA:int, indexB:int, trigger=True):
        '''
            A and B swap their location
        '''
        C = self.__content[indexA]
        self.__content[indexA] = self.__content[indexB]
        self.__content[indexB] = C
        if trigger: self.content_ch.sync_trigger()

    #
    # File Methods
    #

    def save(self) -> None:
        with open(self.__path, "w") as f:
            f.write(
                json.dumps(
                    obj = [song.get_path() for song in self.__content],
                    indent = 4
                )
            )

    def load(self) -> None:
        self.clear()
        with open(self.__path, 'r') as f:
            self.add(
                *json.loads( # Path list
                    f.read()
                ) 
            )
        
        self.content_ch.sync_trigger()

        