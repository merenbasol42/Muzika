import tkinter as tk
import customtkinter as ctk
from tkinter import Misc

from typing import Literal

from tools.tk_tools import IconButton

class StatementPanel(ctk.CTkFrame):
    def __init__(self, root:Misc, icons_dir:str):
        super().__init__(root)

        self.ICONS_DIR:str = icons_dir

        # Eğer fieldlere ihtiyaç kalmazsa kaldırılacak
        self.text_def_song_name = "none text sp"
        self.font = ctk.CTkFont(family="Helvetica", size=14)

        self.bt = tk.Button(self)
        # Widgetlar
        self.mode_icon:IconButton
        self.song_label:ctk.CTkLabel
        self.pause_icon:IconButton

    def set_playing_mode(
            self, 
            keyword:Literal['d', 's', 'p', 'm']
        ):

        match keyword:
            case 'd':
                self.mode_icon.config_icon(
                    *self.preset_param("queue.png")  
                )
            case 's':
                self.mode_icon.config_icon(
                    *self.preset_param("repeat-song.png")  
                )
            case 'p':
                self.mode_icon.config_icon(
                    *self.preset_param("repeat.png")  
                )
            case 'm':
                self.mode_icon.config_icon(
                    *self.preset_param("shuffle.png")  
                )
            case x:
                raise Exception(f"no waaaaaaaaaaay {x} olmaz aga")
        pass

    def set_pause_state(self, target_state:bool):
        if target_state:
            self.pause_icon.config_icon(
                *self.preset_param("pause.png")
            )
        else:
            self.pause_icon.config_icon(
                *self.preset_param("play.png")
            )

    def set_song_label(self, text:str):
        if text is None:
            text = self.text_def_song_name
        self.song_label.configure(
            text=text
        )
 
    def config_texts(self):
        """Metinleri yapılandırmak istiyorsanız en doğrusu song changed'ı bir daha çağırmak"""
        pass

    def display(self):
        self.create_widgets()
        self.pack_widgets()
        self.pack(side="top", fill="x")

    def create_widgets(self):
        self.mode_icon = IconButton(
            self,
            *self.preset_param("queue.png")         
        )
        self.song_label = ctk.CTkLabel(
            self,
            text=self.text_def_song_name,
            font=self.font
        )
        self.pause_icon = IconButton(
            self,
            *self.preset_param("pause.png")
        )

    def pack_widgets(self):
        self.mode_icon.grid(row=0, column=0, padx=10, pady=0)
        self.song_label.grid(row=0, column=1, padx=10, pady=0)
        self.pause_icon.grid(row=0, column=2, padx=10, pady=0)
        self.grid_columnconfigure(1, weight=1)
        
    def preset_param(self, name:str):
        def_icon_path = [self.ICONS_DIR, "statement", name]
        hover = "darker"
        size = (15,15) 
        params = (def_icon_path, hover, size)
        return params