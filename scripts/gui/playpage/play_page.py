from tools import Event, EventWithArgs
from gui.temps.main_page import MainPage 
from .pp_header import PPHeader
from .media_player_frame import MediaPlayerFrame
from .trackbar_frame import TrackBarFrame
from .volume_slider import VolumeSliderFrame

class PlayPage(MainPage):

    def __init__(self, root, icons_dir):
        super().__init__(root=root)

        # Fields
        self._HEADER:PPHeader = PPHeader(self, icons_dir)
        self._MEDIA_PLAYER:MediaPlayerFrame = MediaPlayerFrame(self, self, icons_dir)
        self._TRACKBAR:TrackBarFrame = TrackBarFrame(self)
        self._VOLUME_SLIDER:VolumeSliderFrame = VolumeSliderFrame(self)

        # Events
        # çocukların eventlerini kendi eventlerine eşitler
        self.create_event_shell()

    def config_texts(self):
        self._HEADER.config_texts()
        self._MEDIA_PLAYER.config_texts()
        self._TRACKBAR.config_texts()
        self._VOLUME_SLIDER.config_texts()
        self.song_table.set_column_name(self.text_song_column)

    def postset(self):
        self.song_table.event_bind("queue")
        self.song_table.event_bind("double_click")
        self.text_shell()

    def start(self):
        self._HEADER.start()
        self._HEADER.pack(side="top", fill='x', pady=(0,10))

        self._MEDIA_PLAYER.start()
        self._MEDIA_PLAYER.pack(side="bottom", pady=(0,20))

        self._TRACKBAR.start()
        self._TRACKBAR.pack(side="bottom", pady=10, fill="x")

        self._VOLUME_SLIDER.start()
        self._VOLUME_SLIDER.pack(side="bottom", padx=10, fill="x")

        super().start()

        self.postset()

    #(Kabuk Operasyonu)
    def create_event_shell(self):
        self.edit_page_button_clicked:Event = self._HEADER.edit_button_clicked
        self.settings_button_clicked:Event = self._HEADER.settings_button_clicked
        self.combox_selected:EventWithArgs = self._HEADER.combox_selected

        self.load_button_ck:EventWithArgs = self._MEDIA_PLAYER.load_button_clicked  
        self.mode_button_ck:Event = self._MEDIA_PLAYER.mode_button_clicked
        
        self.prev_button_ck:Event = self._MEDIA_PLAYER.previous_button_clicked
        self.rewind_button_ck:Event = self._MEDIA_PLAYER.rewind_button_clicked
        self.play_button_ck:Event = self._MEDIA_PLAYER.play_pause_button_clicked
        self.forward_button_ck:Event = self._MEDIA_PLAYER.forward_button_clicked
        self.next_button_ck:Event = self._MEDIA_PLAYER.next_button_clicked

        self.pos_track_setted:Event = self._TRACKBAR.user_setted_song_pos
        self.volume_ch:EventWithArgs = self._VOLUME_SLIDER.volume_ch

    def text_shell(self):
        # Table
        self.text_song_column:str = self.song_table.text_song_column

    # (Kabuk Operasyonu)
    # Header Metodları (Sadece Dışarıdan Kullanılanlar) 
    #
    
    def set_pl_list(self, _list:list[str]):
        self._HEADER.set_pl_list(_list)

    # (Kabuk Operasyonu)
    # MediaPlayer Metodları (Sadece Dışarıdan Kullanılanlar) 
    #

    def set_pause_state(self, is_pause:bool):
        self._MEDIA_PLAYER.set_pause_state(is_pause)

    # (Kabuk Operasyonu)
    # Trackbar Metodları (Sadece Dışarıdan Kullanılanlar) 
    #

    def set_song_pos(self, song_pos:float):
        self._TRACKBAR.set_song_pos(song_pos)

    def set_song_length(self, song_length:float):
        self._TRACKBAR.set_song_length(song_length)
