import customtkinter as ctk
from tkinter import Misc

from .sub_menu_page import SubMenuPage
from .sub_menu_page import MyTexts as ParentTexts

class CreditsPage(SubMenuPage):
    def __init__(self, master: Misc):
        super().__init__(master)
        
        self.texts:MyTexts = MyTexts()

        self.scroll_frame:ctk.CTkFrame
        self.content_lbl:ctk.CTkLabel

    def start(self):
        self._create_widgets()
        self._pack_widgets()

    def _create_widgets(self):
        super()._create_widgets()
        self.scroll_frame = ctk.CTkFrame(
            self
        )
        self.content_lbl = ctk.CTkLabel(
            self.scroll_frame, 
            text=self.texts.content,
            wraplength=200
        )
        
    def _pack_widgets(self):
        super()._pack_widgets()
        self.scroll_frame.pack(fill="both", expand=True)
        self.content_lbl.pack(fill='x', pady=(20,0))

    def config_texts(self):
        super().config_texts()
        self.content_lbl.configure(
            text=self.texts.content
        )




class MyTexts(ParentTexts):
    def __init__(self):
        super().__init__()
        self.def_text = "none text pm.cp"
        self.content:str = self.def_text
