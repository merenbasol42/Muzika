import customtkinter as ctk
from typing import Literal

from gui.temps.page import Page
from .sub_menu_page import SubMenuPage
from .main_menu_page import MainMenuPage
from .help_page import HelpPage
from .credits_page import CreditsPage
from .settings_page import SettingsPage


class Menu:
    def __init__(self, root):
        # Fields
        self.root = root
        self.window:ctk.CTkToplevel = ctk.CTkToplevel(
            master = self.root
        )

        # Flags
        self.is_open = False

        # Pages
        self.mmp:MainMenuPage = MainMenuPage(self.window)
        self.hp:HelpPage = HelpPage(self.window)
        self.cp:CreditsPage = CreditsPage(self.window)
        self.sp:SettingsPage = SettingsPage(self.window)
        
        # Preset
        self._mmp_event_binding()
        self._window_setup()
    
    def start(self):
        self.window.wm_transient(self.root)
        self.mmp.start()
        self.hp.start()
        self.cp.start()
        self.sp.start()

    def display(self):
        self.window.deiconify()
        self.mmp.display()
        self.is_open = True

    def undisplay(self):
        self.window.withdraw()
        self.is_open = False

    def config_texts(self):
        self.mmp.config_texts()
        self.hp.config_texts()
        self.cp.config_texts()
        self.sp.config_texts()

    def set_goback_text(self, new_text):
        def asd(page:SubMenuPage):
            page.texts.go_back_button = new_text

        asd(self.hp)
        asd(self.cp)
        asd(self.sp)

    #
    # Diğerleri
    # 

    def _window_setup(self):
        self.window.withdraw()
        self.window.geometry("250x320")
        self.window.title("Menu")
        self.window.protocol("WM_DELETE_WINDOW", self.undisplay)

    #
    # Event Muameleleri
    #

    def _mmp_event_binding(self):
        self.mmp.events.help_button_click.subscribe(
            self._ch_page_event_cb("help")
        )
        self.mmp.events.credits_button_click.subscribe(
            self._ch_page_event_cb("credits")
        )
        self.mmp.events.settings_button_click.subscribe(
            self._ch_page_event_cb("settings")
        )
        self._smp_go_back_binding()

    def _smp_go_back_binding(self):

        def go_back(page:SubMenuPage):
            page.undisplay()
            self.mmp.display()    

        self.hp.go_back_button_clicked.subscribe(
            lambda: go_back(self.hp)
        )
        self.cp.go_back_button_clicked.subscribe(
            lambda: go_back(self.cp)
        )
        self.sp.go_back_button_clicked.subscribe(
            lambda: go_back(self.sp)
        )

    def _ch_page_event_cb(self, keyword:Literal["help", "credits", "settings"]):

        def ch_page(page:Page):
            self.mmp.undisplay()
            page.display()

        match keyword:
            case "help":
                return lambda: ch_page(self.hp)
            case "credits":
                return lambda: ch_page(self.cp)
            case "settings":
                return lambda: ch_page(self.sp)
            case _ :
                raise Exception("aganiga o kadar literal vra")


