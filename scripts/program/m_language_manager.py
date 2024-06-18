from tools import Language as Lang
from tools import LanguageManager as LM
from gui.gui_main import GUI
from utube import MuzikaListDownloader as MLD


class MLanguageManager(LM):
    # Muzika Language Manager
    def __init__(self, path: str, gui:GUI, mld:MLD) -> None:
        super().__init__(path)
        self.gui:GUI = gui
        self.mld:MLD = mld
        self.current_lang:Lang = None
        self.def_text:str = "none text mlm"

    def set_current_lang(self, name:str):
        '''Lang name is lang dir name'''

        a = None
        for lang in self.langs:
            if lang.code == name:
                a = lang

        if a is None:
            raise Exception(f"Bu isimde bir dil paketi yüklü değil: {name}")
        
        self.current_lang = a

    def apply(self):
        if self.current_lang is None:
            raise Exception("Bir dil paketi yüklü değil. Bu yüzden uygulanamaz")
        
        self.__apply_statement_panel()
        self.__apply_play_page()
        self.__apply_edit_page()
        self.__apply_popup_menu()
        self.__apply_mld()

    def __apply_edit_page(self):
        cont = self.current_lang.get_content("edit_page")
        page = self.gui.ep
        
        def header():
            page._HEADER.text_page_title = cont["header"]["title"]
            page._HEADER.text_create_inp = cont["header"]["create_inp"]
            page._HEADER.text_create_inp_title = cont["header"]["create_inp_title"]
            page._HEADER.text_pl_combox_default = cont["header"]["pl_combox"]["default_text"]
            page._HEADER.text_pl_combox_nothing = cont["header"]["pl_combox"]["nothing_text"]
        
        def table():
            page.text_song_column = cont["table"]["song_column"]
        
        def control():
            page._CONTROL_FRAME.text_choose_rb = cont["control"]["choose_rb"]
            page._CONTROL_FRAME.text_queue_rb = cont["control"]["queue_rb"]
            page._CONTROL_FRAME.text_add_button = cont["control"]["add_button"]
            page._CONTROL_FRAME.text_utube_button = cont["control"]["utube_button"]
            page._CONTROL_FRAME.text_remove_button = cont["control"]["remove_button"]

            page._CONTROL_FRAME.text_add_inp = cont["control"]["add_inp"]
            page._CONTROL_FRAME.text_add_inp_title = cont["control"]["add_inp_title"]
            
            page._CONTROL_FRAME.text_utube_inp_title = cont["control"]["utube_inp_title"]
            page._CONTROL_FRAME.text_utube_inp_pl = cont["control"]["utube_inp_pl"]
            page._CONTROL_FRAME.text_utube_inp_url = cont["control"]["utube_inp_url"]
            page._CONTROL_FRAME.text_utube_inp_button = cont["control"]["utube_inp_button"]
                 
            page._CONTROL_FRAME.text_choice_dir = cont["control"]["choice_dir"]
            page._CONTROL_FRAME.text_choice_file = cont["control"]["choice_file"]

        header()
        table()
        control()

    def __apply_play_page(self):
        cont = self.current_lang.get_content("play_page")
        page = self.gui.pp

        def header():
            cheader:dict = cont["header"]
            pheader = page._HEADER

            pheader.text_page_title = cheader["title"]
            pheader.text_pl_combox_default = cheader["pl_combox"]["default_text"]
            pheader.text_pl_combox_nothing = cheader["pl_combox"]["nothing_text"]

        def table():
            page.text_song_column = cont["table"]["song_column"]

        def volume():
            page._VOLUME_SLIDER.text_volume = cont["vol_slider"]["volume"]

        def trackbar():
            ctb = cont["trackbar"]
            ptb = page._TRACKBAR

            ptb.text_song_pos = ctb["song_pos"]
            ptb.text_song_length = ctb["song_length"]

        def control():
            ccontrol = cont["control"]
            pcontrol = page._MEDIA_PLAYER
            pcontrol.text_mode_button = ccontrol["mode_button"]
            pcontrol.text_load_button = ccontrol["load_button"]

        header()
        table()
        volume()
        trackbar()
        control()

    def __apply_statement_panel(self):
        cont = self.current_lang.get_content("statement_panel")
        self.gui.sp.text_def_song_name = cont["default_text"]

    def __apply_popup_menu(self):
        cont = self.current_lang.get_content("popup_menu")
        menu = self.gui.popup_menu
        mmpt = menu.mmp.texts
        
        mmpt.help_button = cont["help"]["button"]
        mmpt.credits_button = cont["credits"]["button"]
        mmpt.settings_button = cont["settings"]["button"]

        menu.set_goback_text(
            cont["go_back_button"]
        )
        menu.hp.texts.content = cont["help"]["content"]        
        menu.cp.texts.content = cont["credits"]["content"]
        menu.sp.texts.lang_lbl = cont["settings"]["lang_lbl"]

    def __apply_mld(self):
        cont = self.current_lang.get_content("utube_toplevel")
        self.mld.text_toplevel_title = cont["title"]
        self.mld.text_toplevel_info = cont["info"]
        self.mld.text_finished = cont["finished"]
        self.mld.texts_downloading = cont["downloading"]

        self.mld.text_error_download = cont["error"]["download"]
        self.mld.text_error_success = cont["error"]["success"]
        self.mld.text_error_input = cont["error"]["input"]

        
