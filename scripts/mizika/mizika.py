from pygame import mixer
from threading import Thread
from random import randint
from time import sleep

from typing import Literal

from tools import Event

from .song import Song
from .playlist import Playlist 
from .util import MizikaCoreError as MCError

mixer.init()    
class Mizika:
    '''
        Temel müzik çalar işlevlerini yerine getiren bir sınıf.

        Aynı paketteki Song, Playlist ve PlaylistList sınıflarını kullanır. 

        Kullanmak için öncelikle <set_playlist> metodu ile bir Playlist\n
    yükleyin. Çalma modunu <set_playing_mode> metodu ile isteğinize göre\n
    değiştirebilirsiniz. Müzik çalmaya <play_song> metodu ile veya <unpause>\n
    metodu ile başlayabilirsiniz.
         
    '''
    
    # Codes
    DEFAULT_MODE = 'd'
    SONG_MODE = 's'
    PLAYLIST_MODE = 'p'
    MIX_MODE = 'm'
    PLAYING_MODE_LIST:list[str] = [DEFAULT_MODE, SONG_MODE, PLAYLIST_MODE, MIX_MODE]

    def __init__(
        self,
        max_history_length:int = 10,
        control_rate:float = 0.2
    ) -> None:

        # Events
        self.song_ch:Event = Event()
        self.mode_ch:Event = Event()
        self.pause_ch:Event = Event()
        self.pos_ch:Event = Event()

        # Fields
        self.__index:int = -1
        self.__pos:float = 0
        self.__mode:str = Mizika.DEFAULT_MODE
        
        self.__pl:Playlist = None
        self.__song:Song = None
        
        self.__history:list[Song] = []
        self.__history_index:int = -1
        
        # Flags
        self.__is_pause:bool = True
        self.__is_running:bool = False
        self.__is_playing_history:bool = False

        # Constant Settings
        self.MAX_HISTORY_LENGTH = max_history_length
        self.CONTROL_RATE = control_rate

        # Thread
        self.__SONG_THREAD:Thread = Thread(target=self.__control)

    #
    # (G/S)etter
    #

    def get_play_index(self) -> int: return self.__index
    def get_pos(self) -> float: return self.__pos
    def get_mode(self) -> chr: return self.__mode
    
    def get_pl(self) -> Playlist: return self.__pl   
    def get_song(self) -> Song: return self.__song
    
    def get_history(self) -> list[Song]: return self.__history 
    def get_history_index(self) -> int: return self.__history_index
    
    def get_pause_state(self) -> bool: return self.__is_pause
    def get_running_state(self) -> bool: return self.__is_running
    def get_history_play_state(self) -> bool: return self.__is_playing_history

    def set_volume(self, percent:float):
        if percent < 0.0 or percent > 100.0: raise MCError("percent must be in 0 to 100")
        mixer.music.set_volume(percent/100.0)

    def set_mode(self, target_mode:Literal['d','s','p','m']):
        '''
            Çalma modunu ayarlar
            Modlar: Mizika.DEFAULT_MODE, Mizika.SONG_MODE, Mizika.PLAYLIST_MODE, Mizika.MIX_MODE
        '''
        self.__mode = target_mode
        # Kontrol yapılacak
        self.mode_ch.sync_trigger()
        
    def set_mode_iterative(self):
        '''
            Çalma modunu ayarlar (İteratif bir şekilde)
            Modlar: Mizika.DEFAULT_MODE, Mizika.SONG_MODE, Mizika.PLAYLIST_MODE, Mizika.MIX_MODE
            
            # Sanırım bu metodu burada yazmamalıydım #
        '''
        list_ = Mizika.PLAYING_MODE_LIST
        index_ = list_.index(self.__mode) + 1
        if index_ == len(list_):
            index_ = 0
        
        self.set_mode(list_[index_]) 
        
    def set_pl(self, playlist:Playlist|None):
        '''<playlist> Playlist nesnesini yükler'''
        self._return_to_start_settings()
        self.__pl = playlist
        if self.__pl is not None: 
            self.__pl.content_ch.subscribe(
                self.pl_content_ch_cb
            )

    def set_is_quit(self, val:bool):
        self.__is_running = val


    #
    # Çalma Metodları
    # 

    def play_song(self, obj:int|Song, save=False):
        '''
            Argumanlardan sadece birini aynı zamanda kullanabilirsin
        '''
        if self.__is_pause:
            self.unpause()

        song:Song = None
        index:int = None

        if type(obj) is Song:
            song = obj
            index = self.__pl.index(song) # Eğer yoksa kodda hata var demek o yüzden safe=False
        else:
            index = obj
            song = self.__pl.get_song(index)
        
        if save: self._save_history(self.__song) # daha song fieldi yenilenmedi

        self.__pos = 0
        self.__index = index
        self.__song = song

        mixer.music.load(song.get_path())
        mixer.music.play()

        self.song_ch.sync_trigger()

    def play_next_song(self):
        ''' Çalma moduna göre sıradaki şarkıyı çalar'''
        if self.__pl is None:
            raise Exception("Yüklü playlist yok")

        pl_len = self.__pl.get_length()

        def mix_f() -> tuple[Song | int, bool]:
            is_playing_on_history = self.__history_index != -1 # geçmişte mi dolaşıyor
            is_overflow_on_history =  self.__history_index == len(self.__history) - 1 #geçmişi aştık mı
            
            if is_playing_on_history: 
                self.__history_index += 1

                if is_overflow_on_history: self.__history_index = -1
                
                else: 
                    try: return self.__history[self.__history_index], False 
                    except Exception: raise MCError(f"olum index {self.__history_index}")

            while True:
                _index = randint(0, pl_len - 1) # randint son sayıyı dahil ediyor
                if _index != self.__index: break

            return _index, True

        def pl_f():
            _index = self.__index + 1
            if _index >= pl_len: # normalde '=='
                _index = 0
            return _index

        def song_f():
            return self.__index 

        def default_f():
            _index = self.__index + 1
            if _index >= pl_len:
                # Hiç birşey yapmasın
                _index = None
                self.pause()
                
            return _index

        obj = None
        save = False

        match self.__mode:

            case Mizika.MIX_MODE:
                obj, save = mix_f()

            case Mizika.PLAYLIST_MODE:
                obj = pl_f()

            case Mizika.SONG_MODE:
                obj = song_f()

            case _: # Hiçbiri değil ise defaulttur. E o da değil ise yine de default gibi davransın 
                obj = default_f()


        if obj is None: return
        self.play_song(obj, save=save)
            
    def play_previous_song(self):
        ''' Çalma moduna göre bir önceki şarkıyı çalar'''

        def mix_f() -> Song:
            history_length = len(self.__history)
            
            #geçmiş boş ise None döndürek bir şey çalmasın
            if history_length == 0: return None 

            # gezinmeye ilk defa başlıyor ise
            elif self.__history_index == -1: self.__history_index = history_length - 1            
            
            # geçmiş listesinin sonunda ise öylece kalsın
            elif self.__history_index == 0: pass

            # Değilse indisi 1 azalt
            else: self.__history_index -= 1

            return self.__history[self.__history_index] 

        def pl_f() -> int:
            new_index = None
            if self.__index == 0: 
                new_index = self.__pl.get_length()
            else:
                new_index = self.__index - 1
            
            return new_index

        def song_f() -> int:
            return self.__index

        def default_f() -> int:
            new_index = None
            if self.__index == 0: 
                self.pause()
            else:          
                new_index = self.__index - 1
            return new_index

        obj = -1
        save = False
        match self.__mode:

            case Mizika.MIX_MODE:
                obj = mix_f()

            case Mizika.PLAYLIST_MODE:
                obj = pl_f()

            case Mizika.SONG_MODE:
                obj = song_f()

            case _: # Hiçbiri değil ise defaulttur. E o da değil ise yine de default gibi davransın 
                obj = default_f()
          
        if obj is None: return
        
        self.play_song(obj, save=save)

    #
    # Sardırma Metodları
    #

    def fast_forward(self, seconds:float):
        ''' Çalan şarkıyı <seconds> saniye kadar ileri sarar '''
        target_pos = self.__pos + seconds
        self.set_pos(target_pos)

    def rewind(self, seconds:float):
        ''' Çalan şarkıyı <seconds> saniye kadar geri sarar'''
        target_pos = self.__pos - seconds
        self.set_pos(target_pos)

    def set_pos(self, target_pos:float):
        ''' Çalan şarkının <target_pos>\' uncu saniyesine gider '''

        """
                Aslında bu kontrolleri burada yapmak istemiyordum ama\n
            bu metodu dışarısı da kullansın 
        """

        if target_pos < 0:
            target_pos = 0
        elif target_pos > self.__song.get_length():
            target_pos = self.__song.get_length()

        mixer.music.set_pos(target_pos)
        self.__pos = target_pos
        self.pos_ch.sync_trigger()
    
    #
    # Setter
    #
        

    #
    # Pause Metodları
    #

    def pause(self):
        mixer.music.pause()
        self.__is_pause = True
        self.pause_ch.sync_trigger()

    def unpause(self):
        mixer.music.unpause()
        self.__is_pause = False
        self.pause_ch.sync_trigger()

    def pause_toggle(self):
        if self.__is_pause: self.unpause()
        else: self.pause()


    #
    # Diğerleri
    #

    def __control(self):
        '''
            Bu method private seviyesindedir. Dışarıdan kullanmayınız.

            Mizika işlevleri için sürekli <self.CONTROL_RATE> saniye aralığıyla dönen\n
        bir control döngüsü metodu.
            Bu döngüyü, __init__ metodu içinde tanımlanıp başlatılmış olan <self.SONG_THREAD>\n
        döndürür.
            Bu döngü <self.is_running> değişkeninin değeri True olunca kırılır ve thread de \n
        boşa düşer(yok olur).
        '''
        while self.__is_running:
            if not self.__is_pause: 
                if not mixer.music.get_busy():
                    self.play_next_song()
                else:
                    self.__pos += self.CONTROL_RATE
                    self.pos_ch.sync_trigger()
            sleep(self.CONTROL_RATE)

    def _save_history(self, song):
        '''
            Bu method protected seviyesindedir. Dışarıdan kullanmayınız.

            Verilen <song> Song nesnesini geçmişe kaydeder

            Geçmiş, <self.MAX_HISTORY_LENGTH> uzunluğunu aşarsa ilk baştaki\n
        geçmiş şarkıyı siler
        '''
        if song is None: return
        self.__history.append(song)
        if len(self.__history) == self.MAX_HISTORY_LENGTH: # Eğer max uzunluğu aşmışsak
            self.__history.pop(-1) # Sonuncuyu silelim

    def _return_to_start_settings(self):
        # Fields
        self.__index:int = -1
        self.__pos:float = 0
        self.__mode:str = Mizika.DEFAULT_MODE
        
        self.__pl:Playlist = None
        self.__song:Song = None
        
        self.__history:list[Song]
        self.__history_index:int = -1
        
        # Flags
        self.__is_pause = True
        # self.__is_running:bool = False
        self.__is_playing_history:bool = False

        mixer.music.stop()
        self.song_ch.sync_trigger()
        self.mode_ch.sync_trigger()
        self.pause_ch.sync_trigger()
        self.pos_ch.sync_trigger()

    def start(self):
        self.__is_running = True
        self.__SONG_THREAD.start()

    def stop(self):
        self.__is_running = False
        mixer.music.stop()
        
    #
    # 
    #

    def pl_content_ch_cb(self):

        # Current song control
        if self.__pl is None or self.__song is None: return


        res = self.__pl.index(self.__song)
        
        if res is None:
            self.set_pl(self.__pl) # Yeniden yükle

        else: self.__index = res

        # History control
        for song in self.__history:
            if self.__pl.index(song, safe=True) is None:
                self.__history.remove(song)



