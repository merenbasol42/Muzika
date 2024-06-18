from tkinter import Misc
import customtkinter as ctk

from tools import EventWithArgs
from .sub_menu_page import SubMenuPage
from .sub_menu_page import MyTexts as ParentTexts



class SettingsPage(SubMenuPage):
    def __init__(self, master: Misc):
        super().__init__(master)

        # Fields
        self.lang_list:list[str] = ["none lang wtf >:("]

        # Texts
        self.texts:MyTexts = MyTexts()

        # Widgets
        self.sc_frame:ctk.CTkScrollableFrame
        self.lang_lbl:ctk.CTkLabel
        self.lang_combox:ctk.CTkComboBox

        # Events
        self.combox_selected:EventWithArgs = EventWithArgs()

    def start(self):
        self._create_widgets()
        self._pack_widgets()

    def _create_widgets(self):
        super()._create_widgets()
        self.sc_frame = ctk.CTkScrollableFrame(
            self
        )
        self.lang_lbl = ctk.CTkLabel(
            self.sc_frame, text=self.texts.lang_lbl, wraplength=200
        )
        self.lang_combox = ctk.CTkComboBox(
            self.sc_frame, values=self.lang_list, command=self._combobox_selected_cb
        )

    def _pack_widgets(self):
        super()._pack_widgets()
        self.sc_frame.pack(fill="both", expand=True)
        self.lang_lbl.pack(pady=(20,20))
        self.lang_combox.pack(pady=20)

    #
    # Dış Erişim
    #

    def set_lang_list(self, _list:list[str]):
        self.lang_list = _list
        self.lang_combox.configure(values=self.lang_list)

    def set_lang(self, lang_code:str):
        self.lang_combox.set(lang_code)

    def config_texts(self):
        super().config_texts()
        self.lang_lbl.configure(
            text=self.texts.lang_lbl
        )

    #
    # Callbacks
    #

    def _combobox_selected_cb(self, event=None):
        lang_code_ = self.lang_combox.get()
        self.combox_selected.sync_trigger(
            lang_code_
        )


class MyTexts(ParentTexts):
    def __init__(self):
        super().__init__()
        self.def_text = "none text pm.sp"
        self.lang_lbl = self.def_text
    
