import os
import json

from tools.funcs import get_file_paths_in_dir
from tools.events import Event

from .playlist import Playlist
from .util import MizikaPLListError as PLLError

class PLList:
    def __init__(self, path:str) -> None:
        if os.path.isfile(path):
            raise PLLError("Playlist list's path can't be a file. Must be directory")

        self.__path:str = path
        self.__length:int = 0
        self.__content:list[Playlist] = [] 

        self.content_ch:Event = Event()

    #
    # Getters
    #

    def get_path(self) -> str:
        return self.__path 

    def get_pl(self, index:int) -> Playlist:
        try:
            return self.__content[index]
        except Exception as e:
            raise PLLError(e)

    def get_content(self) -> list[Playlist]:
        return self.__content

    def get_length(self) -> int:
        return self.__length
    
    #
    # contetn
    #

    def index(self, name:str):
        for pl in self.__content:
            if pl.get_name() == name: 
                return self.__content.index(pl)

    #
    # Playlist File Methods
    #

    def create(self, name:str):
        '''
            do not add '.json' at the end.
        '''
        name += ".json"
        path = os.path.join(self.__path, name)
        if os.path.exists(path):
            raise PLLError("A playlist with this name already exists")
        
        with open(path, "w") as f:
            f.write(
                json.dumps(
                    [], indent=4
                )
            )
        
        self.__content.append(
            Playlist(path)
        )
        self.__length += 1
        self.content_ch.sync_trigger()

    def delete(self, index:int = None, obj:Playlist = None):
        print("bıktım")
        if index is None:
            try:
                index = self.__content.index(obj)
            except Exception as e:
                raise PLLError(e)

        os.remove(
            self.get_pl(index).get_path()
        )
        self.__content.pop(index)
        self.__length -= 1
        self.content_ch.sync_trigger()
        
    def rename(self, new_name:str, index:int = None, obj:Playlist = None):
        '''
            do not add '.json' at the end.
        '''

        if new_name is None or new_name.strip() == "":
            raise PLLError("u gave nothing for rename. give me something")

        if index is None:
            try:
                index = self.__content.index(obj)
            except Exception as e:
                raise PLLError(e)

        new_name += ".json"
        old_path = self.__content[index].get_path() 
        new_path = os.path.join(
            self.__path, new_name
        )

        if os.path.exists(new_path):
            raise PLLError("A playlist with this name already exists")

        os.rename(
            src = old_path,
            dst = new_path
        )
        
        self.get_pl(index)._set_path(
            new_path = new_path
        )

    #
    # File Methods
    #
    
    def load(self):
        '''
            playlists klasöründeki tüm playlistleri yükler
        '''
        self.__content = [Playlist(path) for path in get_file_paths_in_dir(self.__path)]
        for pl in self.__content:
            pl.load()
            self.__length += 1
        self.content_ch.sync_trigger()

    def save_all(self):
        for pl in self.__content: pl.save()