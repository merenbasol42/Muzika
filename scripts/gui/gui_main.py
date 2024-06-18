import customtkinter as ctk

from typing import Literal

from tools import Event
from tools.tk_tools import RowNavigator

from .playpage.play_page import PlayPage
from .editpage.edit_page import EditPage
from .statement_panel import StatementPanel
from .popup_menu.popup_menu import Menu



class GUI:
    def __init__(self, icons_dir) -> None:
        self.root = ctk.CTk()

        self.pp = PlayPage(self.root, icons_dir)
        self.ep = EditPage(self.root, icons_dir, self.root)
        self.sp = StatementPanel(self.root, icons_dir)
        self.popup_menu:Menu = Menu(self.root)

        self.nav = RowNavigator(self.root)
        self.wn_width:int = 450
        self.wn_height:int = 700

        #Events
        self.quited:Event = Event() 
        self.root.bind("<Destroy>", self._quited_cb)
        self._event_binding()

    def preset(self):
        self.root.title("Muzika")
        self.root.geometry(f"{self.wn_width}x{self.wn_height}")
        self.root.resizable(False, False)

    def start(self):
        self.preset()
        self.ep.start()
        self.pp.start()
        self.popup_menu.start()

        self.sp.display()
        self.nav.first_page_show(self.pp)

    def config_texts(self):
        self.ep.config_texts()
        self.pp.config_texts()
        self.popup_menu.config_texts()
        
    def _event_binding(self):
        self._pp_event_binding()
        self._ep_event_binding()
        
    def _pp_event_binding(self):
        self.pp.edit_page_button_clicked.subscribe(
            self._pp_event_cbs("go_edit")
        )
        self.pp.settings_button_clicked.subscribe(
            self._pp_event_cbs("settings")
        )

    def _ep_event_binding(self):
        self.ep.play_page_button_clicked.subscribe(
            self._ep_event_cbs("go_pp")
        )
        self.ep.settings_button_clicked.subscribe(
            self._ep_event_cbs("settings")
        )
        
    #
    # Callbacks
    #
        
    def _pp_event_cbs(self, keyword:Literal["go_edit", "settings"]):
        def go_edit():
            self.nav.pass_page(self.pp, self.ep, "left")
            
        def settings():
            # Bu kodu customtkinter dokumantasyonundan çaldım
            if not self.popup_menu.is_open:
                self.popup_menu.display()
            else:
                self.popup_menu.undisplay()

        match keyword:
            case "go_edit":
                return go_edit
            case "settings":
                return settings
            case _:
                raise Exception("Aga niga o kadar literal var")

    def _ep_event_cbs(self, keyword:Literal["go_pp", "settings"]):
        def go_pp():
            self.nav.pass_page(self.ep, self.pp, "right")

        def settings():
            # Bu kodu customtkinter dokumantasyonundan çaldım
            if not self.popup_menu.is_open:
                self.popup_menu.display()
            else:
                self.popup_menu.undisplay()

        match keyword:
            case "go_pp":
                return go_pp
            case "settings":
                return settings
            case _:
                raise Exception("Aga niga o kadar literal var")

    def _quited_cb(self, event=None):
        self.quited.sync_trigger()

    #
    # Diğerleri
    #


        
