import customtkinter as ctk
from tkinter import Misc

from tools import Event
from gui.temps import Page


class SubMenuPage(Page):
    def __init__(self, master: Misc):
        super().__init__(master)
        self.go_back_button_clicked:Event = Event()
        self.go_back_button:ctk.CTkButton 
        self.texts:MyTexts = MyTexts()
    
    def _create_widgets(self):
        self.go_back_button = self.create_smp_button(
            text=self.texts.go_back_button, cb=self._go_back_button_cb
        )

    def _pack_widgets(self):
        self.go_back_button.pack(side="bottom", pady=(10,15))

    def display(self):
        self.pack(
            fill = "both",
            expand = True,
            pady = (10,10),
            padx = (10,10)
        )

    def config_texts(self):
        self.go_back_button.configure(
            text=self.texts.go_back_button
        )

    def create_smp_button(self, master=None, text="", cb=None):
        if master is None:
            master = self
        
        return ctk.CTkButton(
            master = master,
            command = cb,
            text=text,
            width = 70,
            height = 30
        ) 

    def _go_back_button_cb(self):
        self.go_back_button_clicked.sync_trigger()


class MyTexts:
    def __init__(self) -> None:
        self.def_text:str = "none text smp"
        self.go_back_button:str = self.def_text