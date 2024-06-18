import customtkinter as ctk
from tkinter import Misc

from .sub_menu_page import SubMenuPage
from .sub_menu_page import MyTexts as ParentTexts

class HelpPage(SubMenuPage):
    def __init__(self, master: Misc):
        super().__init__(master)

        # Fields
        # override
        self.texts:MyTexts = MyTexts()
        
        # Widgets
        self.text_frame:ctk.CTkScrollableFrame
        self.help_lbl:ctk.CTkLabel

    def start(self):
        self._create_widgets()
        self._pack_widgets()

    def config_texts(self):
        super().config_texts()
        self.help_lbl.configure(
            text=self.texts.content
        )

    def _create_widgets(self):
        super()._create_widgets()
        self.text_frame = ctk.CTkScrollableFrame(self)
        self.help_lbl = ctk.CTkLabel(
            self.text_frame, text=self.texts.content, wraplength=200
        )

    def _pack_widgets(self):
        super()._pack_widgets()
        self.help_lbl.pack()
        self.text_frame.pack(fill="both", expand=True)

class MyTexts(ParentTexts):
    def __init__(self) -> None:
        super().__init__()
        self.def_text = "none text pm.hp"
        self.content:str =  self.def_text