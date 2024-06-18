from tkinter import Misc
import customtkinter as ctk

from tools import Event

from gui.temps import Page

class MainMenuPage(Page):
    def __init__(self, master: Misc):
        super().__init__(master)
        
        # Fields
        self.texts:MyTexts = MyTexts()        
        self.events:MyEvents = MyEvents()

        # Widgets
        self.help_button:ctk.CTkButton
        self.credits_button:ctk.CTkButton
        self.settings_button:ctk.CTkButton

    def start(self):
        self.create_widgets()
        self.pack_widgets()

    def display(self):
        self.pack(
            pady = (20,20),
            padx = (20,20),
            fill = "both",
            expand = True
        )

    def create_widgets(self):
        self.help_button = self.create_mm_button(
            text=self.texts.help_button,
            cb=self._help_button_cb
        )
        self.credits_button = self.create_mm_button(
            text=self.texts.credits_button,
            cb=self._credits_button_cb
        )
        self.settings_button = self.create_mm_button(
            text=self.texts.settings_button,
            cb=self._settings_button_cb
        )

    def pack_widgets(self):
        self.help_button.pack(side="top", pady=(20,0))
        self.credits_button.pack(side="top", pady=(20,0))
        self.settings_button.pack(side="top", pady=(20,0))

    def create_mm_button(self, master=None, cb=None, text=""):
        button = ctk.CTkButton(
            master or self,
            command=cb,
            text=text,
            width=140,
            height=40
        )
        return button
    
    #
    # Dış Erişim 
    #

    def config_texts(self):
        self.help_button.configure(
            text=self.texts.help_button
        )
        self.credits_button.configure(
            text=self.texts.credits_button
        )
        self.settings_button.configure(
            text=self.texts.settings_button
        )

    #
    # Callbacks
    #

    def _help_button_cb(self):
        self.events.help_button_click.sync_trigger()

    def _credits_button_cb(self):
        self.events.credits_button_click.sync_trigger()
    
    def _settings_button_cb(self):
        self.events.settings_button_click.sync_trigger()

###
#
# Field Grouping Class
#
###

class MyTexts:
    def __init__(self):
        self.DEF_TEXT:str = "none text pm.mmp"
        self.help_button:str =  self.DEF_TEXT
        self.credits_button:str = self.DEF_TEXT
        self.settings_button:str = self.DEF_TEXT

class MyEvents:
    def __init__(self):
        self.help_button_click:Event = Event()
        self.credits_button_click:Event = Event()
        self.settings_button_click:Event = Event()