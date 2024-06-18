import os
from typing import Literal

from tools import Event

from .mizika import Mizika
from .playlist_list import PLList 
from .playlist import Playlist
from .util import MizikaManagerError as MMError


class MizikaManager:
    '''
        MizikaManager, Mizika paketinin tüm özelliklerini bir arada kullanmak için\n
        oluşturulmuş 'toplama' bir sınıftır. Ek özellik olarak sadece playlists klsörünün\n
        varlığını kontrol eder, yoksa oluşturur.
    '''

    def __init__(
        self,
        running_dir:str = None,
        playlist_dir:str = None
    ):

        # Constants
        if running_dir is None: # bu dosyanın bulunduğu yer olsun
            running_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
        
        self.RUNNING_DIR:str = running_dir

        if playlist_dir is None: # playlist klasörü oluşturulsun
            playlist_dir = os.path.join(self.RUNNING_DIR, "playlists") 
            
            try: os.mkdir(playlist_dir)
            except Exception: pass # Zaten ötle bir klasör varsa hiç bişi yapmasın
  
        self.PLAYLISTS_DIR:str = playlist_dir

        # Fields
        self.MIZIKA:Mizika = Mizika()
        self.pl_list:PLList = PLList(self.PLAYLISTS_DIR)
        self.edit_pl:Playlist = None
        self.play_pl:Playlist = None

        # Events
        self.edit_pl_ch:Event = Event()
        self.play_pl_ch:Event = Event()
        self.edit_pl_content_ch:Event = Event() # Köprü/kabuk event
        self.play_pl_content_ch:Event = Event() # Köprü/kabuk event

    def set_edit_pl(self, index:int):
        try: pl = self.pl_list.get_pl(index) 
        except Exception as e: raise MMError(e)
        # Artık eskisi kullanımda olmayacağından onunla event bağlantısını koparıyoruz
        if self.edit_pl is not None:
            self.edit_pl.content_ch.describe(
                self.edit_pl_content_ch.sync_trigger
            )
            # self.edit_pl.save()
        self.edit_pl = pl
        # self.edit_pl.load() Zaten loadluyoruz hepsini
        # Yenisi ile event bağlantısı kuruyoruz
        self.edit_pl.content_ch.subscribe(
            self.edit_pl_content_ch.sync_trigger
        )

        self.edit_pl_ch.sync_trigger()

    def set_play_pl(self, index:int):
        try: pl = self.pl_list.get_pl(index) 
        except Exception as e: raise MMError(e)

        # Artık eskisi kullanımda olmayacağından onunla event bağlantısını koparıyoruz
        if self.play_pl is not None:
            self.play_pl.content_ch.describe(
                self.play_pl_content_ch.sync_trigger
            )
            # self.play_pl.save()
        self.MIZIKA.set_pl(pl)
        self.play_pl = pl
        self.play_pl.load()
        # Yenisi ile event bağlantısı kuruyoruz
        self.play_pl.content_ch.subscribe(
            self.play_pl_content_ch.sync_trigger
        )

        self.play_pl_ch.sync_trigger()

    def get_path_list(self, pl:Literal["edit", "play"]) -> list[str]:
        '''
            This method return a pathlist from playlist what get <pl> param
        '''
        match pl:
            case "edit": return self.edit_pl.get_path_list() if self.edit_pl else None
            case "play": return self.play_pl.get_path_list() if self.play_pl else None

