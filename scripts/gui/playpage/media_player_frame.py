import customtkinter as ctk
from tkinter import Misc
from os.path import join

from tools.events import Event, EventWithArgs
from tools.tk_tools import ask_int_input
from tools.tk_tools import create_space
from tools.tk_tools import IconButton


class MediaPlayerFrame(ctk.CTkFrame):
    
    def __init__(self, master:Misc, root:Misc, icons_dir:str):
        super().__init__(master=master)
        # Kök widget yani pencere
        self.root:Misc = root
        self.ICONS_DIR:str = icons_dir
        self.MP_ICONS_DIR:str = join(icons_dir,"mediaplayer")

        # Events
        self.previous_button_clicked = Event()
        self.rewind_button_clicked = Event()
        self.play_pause_button_clicked = Event()
        self.forward_button_clicked = Event()
        self.next_button_clicked = Event()

        self.mode_button_clicked = Event()
        self.load_button_clicked:EventWithArgs = EventWithArgs()

        # Fields
        self.is_pause:bool = True

        # Texts
        self.DEF_TEXT:str = "none text pp.media"
        self.text_mode_button:str = self.DEF_TEXT
        self.text_load_button:str = self.DEF_TEXT

        # Widgets        
        self.previous_button:IconButton
        self.rewind_button:IconButton
        self.play_button:IconButton
        self.forward_button:IconButton
        self.next_button:IconButton

        self.mode_button:IconButton
        self.load_button:IconButton

        self.top_frame:ctk.CTkFrame
        self.bot_frame:ctk.CTkFrame

    def start(self):
        self.top_frame = ctk.CTkFrame(self)
        self.bot_frame = ctk.CTkFrame(self)
        self.create_buttons()
        self.pack_buttons()
        self.top_frame.pack(side="top", pady=5)
        self.bot_frame.pack(side="top")
        # create_space(master=self).pack(pady=20)

    def create_buttons(self):
        self.previous_button = self.__create_media_player_button(
            master=self.top_frame,
            icon_name="previous",
            cb=self.__previous_button_cb
        )
        self.rewind_button = self.__create_media_player_button(
            master=self.top_frame,
            icon_name="rewind",
            cb=self.__rewind_button_cb
        )
        self.play_button = self.__create_media_player_button(
            master=self.top_frame,
            icon_name="play",
            cb=self.__play_button_cb,
            size=(60,60)
        )
        self.forward_button = self.__create_media_player_button(
            master=self.top_frame,
            icon_name="fast-forward",
            cb=self.__forward_button_cb
        )
        self.next_button = self.__create_media_player_button(
            master=self.top_frame,
            icon_name="next",
            cb=self.__next_button_cb
        )

        self.mode_button = self.__create_bot_button(
            master=self.bot_frame,
            text=self.text_mode_button,
            cb=self.__mode_button_cb
        )
        self.load_button = self.__create_bot_button(
            master=self.bot_frame,
            text=self.text_load_button,
            cb=self.__load_button_cb
        )

    def pack_buttons(self):
        self.previous_button.pack(side="left")
        self.rewind_button.pack(side="left", padx=20)
        self.play_button.pack(side="left")
        self.forward_button.pack(side="left", padx=20)
        self.next_button.pack(side="left")
        
        self.mode_button.pack(side="left")
        create_space(master=self.bot_frame).pack(side="left", padx=50)
        self.load_button.pack(side="left")

    def __create_media_player_button(
        self,
        icon_name:str,
        master=None, 
        cb=None, 
        size=(40,40)
    ) -> IconButton:
        if not master:
            master = self

        def_icon_path, hover_icon_path = self._get_icon_paths(icon_name)

        return IconButton(
            master=master,
            def_icon_path=def_icon_path,
            hover="darker",
            command=cb,
            size=size
        )

    def __create_bot_button(self, master, text:str="none", cb=None) -> ctk.CTkButton:
        return ctk.CTkButton(
            master=master,
            text=text,
            width=70,
            height=30,
            command=cb
        )

    #
    # Dış Erişim
    #

    def set_pause_state(self, is_pause:bool):
        self.is_pause = is_pause
        if is_pause:
            self.play_button.config_icon(
                self._get_icon_paths("play")[0],
                new_hover="darker",
                size=(60,60)
            )
        else:
            self.play_button.config_icon(
                self._get_icon_paths("pause")[0],
                new_hover="darker",
                size=(60,60)
            )

    #
    # Callbacks
    #

    def __previous_button_cb(self):
        self.previous_button_clicked.sync_trigger()

    def __rewind_button_cb(self):
        self.rewind_button_clicked.sync_trigger()

    def __play_button_cb(self):
        self.play_pause_button_clicked.sync_trigger()

    def __forward_button_cb(self):
        self.forward_button_clicked.sync_trigger()

    def __next_button_cb(self):
        self.next_button_clicked.sync_trigger()
    
    def __mode_button_cb(self):
        self.mode_button_clicked.sync_trigger()

    def __load_button_cb(self):
        # Girdi kontrolü
        _id = ask_int_input(
            parent=self.root, #Pencerenin ortasında gözüksün
            inp_text="Yüklemek istediğiniz şarkının adını giriniz"
        )
        if _id == None:
            return
        self.load_button_clicked.sync_trigger(_id) #Argümanlı haa

    # Diğerleri
    
    def _get_icon_paths(self, icon_name:str):
        def_icon_path = [
            self.MP_ICONS_DIR,
            f"{icon_name}.png"
        ]
        hover_icon_path = [
            self.MP_ICONS_DIR,
            f"{icon_name}(hover).png"
        ]

        return (def_icon_path, hover_icon_path)

    def config_texts(self):
        self.mode_button.configure(
            text=self.text_mode_button
        )
        self.load_button.configure(
            text=self.text_load_button
        )