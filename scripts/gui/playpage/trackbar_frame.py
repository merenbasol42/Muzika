import customtkinter as ctk
from tools import EventWithArgs

class TrackBarFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        #Events
        self.user_setted_song_pos:EventWithArgs = EventWithArgs()

        #Fields
        self.song_length:float = 0.0
        self.is_on_click = False

        #Text
        self.DEF_TEXT:str = "none text pp.tb"
        self.pre_text_pos:str = self.DEF_TEXT
        self.pre_text_length:str = self.DEF_TEXT
        self.text_song_pos:str = self.DEF_TEXT
        self.text_song_length:str = self.DEF_TEXT

        #Widgets
        self.trackbar:ctk.CTkSlider
        self.song_pos_lbl:ctk.CTkLabel
        self.song_length_lbl:ctk.CTkLabel
        self.song_length_pos_frame:ctk.CTkFrame

    def start(self):
        self.create_widgets()
        self.pack_widgets()

        self.trackbar.bind("<Button-1>", self.__trackbar_on_click)
        self.trackbar.bind("<ButtonRelease-1>", self.__trackbar_on_release)
        self.trackbar.set(0.0)

    def create_widgets(self) -> None:
        self.trackbar = ctk.CTkSlider(
            master=self,
            from_=0, to=100,
            orientation="horizontal",
            width=400,
            height=20
        )

        self.song_length_pos_frame = ctk.CTkFrame(self)

        self.song_pos_lbl = ctk.CTkLabel(
            master=self.song_length_pos_frame,
            text=self.text_song_pos,
            padx=20
        )

        self.song_length_lbl = ctk.CTkLabel(
            master=self.song_length_pos_frame,
            text=self.text_song_length,
            padx=20
        )

    def pack_widgets(self):
        self.trackbar.pack(side="bottom", pady=10)
        self.song_pos_lbl.pack(side="left")
        self.song_length_lbl.pack(side="right")
        self.song_length_pos_frame.pack(side="bottom", fill="x",expand=True)

    #
    #
    #
        
    def set_song_pos(self, song_pos:float):
        if not self.is_on_click:
            if self.song_length == 0.0:
                percent = 0.0
            else:
                percent = (song_pos/self.song_length)*100
            
            self.__set_trackbar(percent)
            self.song_pos_lbl.configure(
                text=self.__seconds_to_text(song_pos)
            )

    def set_song_length(self, song_length:float):
        self.song_length = song_length
        text = self.__seconds_to_text(song_length)
        self.song_length_lbl.configure(
            text=text
        )

    def __set_trackbar(self, percent):
        self.trackbar.set(percent)
    
    def __seconds_to_text(self, seconds:float):
        minutes = int(seconds // 60)
        kalan_saniye = int(seconds % 60)
        return "{}:{:02d}".format(minutes, kalan_saniye)


    #
    # Callbacks
    #

    def __trackbar_on_click(self, event):
        self.is_on_click = True

    def __trackbar_on_release(self, event):
        val = self.song_length * self.trackbar.get() / 100
        self.user_setted_song_pos.sync_trigger(val)
        self.is_on_click = False


    def config_texts(self):
        if self.song_pos_lbl._text == self.pre_text_pos:
            self.song_pos_lbl.configure(
                text=self.text_song_pos
            )
        
        self.pre_text_pos = self.text_song_pos

        if self.song_length_lbl._text == self.pre_text_length:
            self.song_length_lbl.configure(
                text=self.text_song_length
            )
        
        self.pre_text_length = self.text_song_length