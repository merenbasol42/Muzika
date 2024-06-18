import customtkinter as ctk

from tools import Event, EventWithArgs 
from tools.tk_tools import IconButton


class Header(ctk.CTkFrame):
    def __init__(self, master, icons_dir):
        super().__init__(master)

        #Events
        self._left_header_button_clicked:Event = Event()
        self.settings_button_clicked:Event = Event()
        self.combox_selected:EventWithArgs = EventWithArgs()

        #Consts
        self.DEF_TEXT:str = "none text"

        #Fields
        self.ICONS_DIR:str = icons_dir    

        self.pl_list:list[str] = ["playlist1", "playlist2", "playlist3"] 
        self.current_pl_index:int = -1

        #Texts
        self.text_page_title = self.DEF_TEXT
        self.text_pl_combox_nothing = self.DEF_TEXT
        self.text_pl_combox_default = self.DEF_TEXT

        #Flags
        self.flag = False

        #Widgets
        self._left_header_button:IconButton = None
        self.settings_button:IconButton
        
        self.mid_frame:ctk.CTkFrame
        self.page_title_label:ctk.CTkLabel
        self.pl_combobox:ctk.CTkComboBox

    #
    # Varlık Metodları
    #

    def start(self):
        self.create_widgets()
        self.pack_widgets()
        self.pl_combobox.set(self.text_pl_combox_default)

    def create_widgets(self):
        self._left_header_button = self._create_navigation_button(
            def_path="edit.png",
            cb=self._left_header_button_cb
        ) 
        self.settings_button = self._create_navigation_button(
            def_path="settings.png",
            cb=self._settings_button_cb
        ) 

        self.mid_frame = ctk.CTkFrame(self)
        self.page_title_label = ctk.CTkLabel(
            self.mid_frame, text=self.text_page_title
        )
        self.pl_combobox = ctk.CTkComboBox(
            self.mid_frame, values=self.pl_list, command=self._combobox_selected_cb
        )

    def pack_widgets(self):
        self._left_header_button.pack(side="left", padx=20)
        self.settings_button.pack(side="right", padx=20)
        self.page_title_label.pack(side="top")
        self.pl_combobox.pack(fill="x", expand=False, padx=20)
        self.mid_frame.pack(fill="x", padx=0)


    def _create_navigation_button(self, def_path:str, master=None, cb=None):
        _def_path:list[str] = [self.ICONS_DIR, "navigation", def_path]
        if master is None:
            master = self
        return IconButton(
            master=master,
            command=cb,
            def_icon_path=_def_path,
            hover="darker",
            size=(30,30)
        )

    #
    # Dış Erişim Metodları
    #

    def set_pl_list(self, _list:list[str]):
        # if self.flag:
        #     return
        # self.flag = True

        self.pl_list = _list
        if len(self.pl_list) == 0:
            self.pl_combobox.set(self.text_pl_combox_nothing)
        else:
            if self.pl_list.count(self.pl_combobox.get()) == 0:
                self.pl_combobox.set(self.text_pl_combox_default)
        self.pl_combobox.configure(values=self.pl_list)
        # self.flag = False

    def set_combobox_index(self, index:int):
        val:str = self.pl_list[index]
        self.pl_combobox.set(val)
        self.current_pl_index = index

    #
    # Callbacks
    #
    
    def _left_header_button_cb(self):
        self._left_header_button_clicked.sync_trigger()

    def _settings_button_cb(self):
        self.settings_button_clicked.sync_trigger()

    def _combobox_selected_cb(self, event=None):
        index = self.pl_list.index(self.pl_combobox.get())
        self.current_pl_index = index
        self.combox_selected.sync_trigger(index)

    #
    # Diğerleri
    #

    def config_texts(self):
        self.page_title_label.configure(
            text=self.text_page_title
        )
        #pl combox default ve pl combox nothing metinlerini yapılandırmaya gerek yok
        self.set_pl_list(self.pl_list) #Bu pl_combox metinlerini eğer eskisi duruyorsa yenilemeye yarar
