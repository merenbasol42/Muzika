import customtkinter as ctk

from tools import Event, EventWithArgs
from tools.tk_tools import ask_str_input
from tools.tk_tools import IconButton
from gui.temps import Header


class EPHeader(Header):
    def __init__(self, master, icons_dir):
        super().__init__(master, icons_dir)

        #Events
        # combobox_selected parent sınıfında tanımlı
        self.go_back_button_clicked:Event = self._left_header_button_clicked
        self.delete_pl_button_clicked:Event = Event()
        self.create_pl_button_clicked:EventWithArgs = EventWithArgs()

        #Consts
        self.DEF_TEXT = "none text ep.header"

        #Fields
        self.text_page_title = self.DEF_TEXT
        self.text_create_inp = self.DEF_TEXT
        self.text_create_inp_title = self.DEF_TEXT
        self.text_pl_combox_default = self.DEF_TEXT
        self.text_pl_combox_nothing = self.DEF_TEXT

        #Widgets
        self.go_play_page_button:IconButton = self._left_header_button
        self.delete_pl_button:IconButton
        self.create_pl_button:IconButton
        self.pl_frame:ctk.CTkFrame

    def config_texts(self):
        super().config_texts()
        #create inp ve create inp title metinlerini yapılandırmaya gerek yok

    def start(self):
        self.create_widgets()
        self.pack_widgets()
        self.pl_combobox.set(self.text_pl_combox_default)
    
    def create_widgets(self):
        super().create_widgets()

        self.pl_frame = ctk.CTkFrame(self.mid_frame)
        # pl_frame içinde olsun diye tekrar yarattık
        self.pl_combobox = ctk.CTkComboBox(
            self.pl_frame,
            values=self.pl_list,
            command=self._combobox_selected_cb
        )
        self.delete_pl_button = self.create_pl_frame_button(
            cb=self._delete_pl_button_cb,
            icon_name="delete"
        )
        self.create_pl_button = self.create_pl_frame_button(
            cb=self._create_pl_button_cb,
            icon_name="create"
        )
        self._left_header_button.config_icon(
            new_def_path=[self.ICONS_DIR, "navigation", "play-page.png"],
            new_hover="darker",
            size=(30,30)
        )

    def pack_widgets(self):
        super().pack_widgets()
        self.mid_frame.pack_forget()
        self.pl_frame.pack_forget()
        self.pl_combobox.pack_forget()
        
        self.delete_pl_button.pack(side="right")
        self.create_pl_button.pack(side="left")
        self.pl_combobox.pack(fill="x", expand=False, padx=5)
        self.pl_frame.pack(side="top", fill="x", expand=False, padx=20)
        self.mid_frame.pack(fill="x", padx=0)

    def create_pl_frame_button(
            self,
            icon_name:str,
            cb=None,
            master=None,
            size=(25,25)
        ):
        if master is None:
            master = self.pl_frame

        a = self._get_icon_paths(icon_name)
        return IconButton(
            master=master,
            def_icon_path= a[0],
            hover="darker",
            command=cb,
            size=size
        )
    
    #
    # Callbacks
    #

    def _delete_pl_button_cb(self):
        current_pl = self.pl_combobox.get()
        def_text = self.text_pl_combox_default
        none_text = self.text_pl_combox_nothing
        if current_pl == def_text or current_pl == none_text:
            return
        self.pl_combobox.set(self.text_pl_combox_default)
        self.delete_pl_button_clicked.sync_trigger()

    def _create_pl_button_cb(self):
        _inp = ask_str_input(
            self.master,
            inp_title=self.text_create_inp_title,
            inp_text=self.text_create_inp
        )
        if _inp is None: return

        self.create_pl_button_clicked.sync_trigger(_inp)



    def _settings_button_cb(self):
        super()._settings_button_cb()

    def _combobox_selected_cb(self, event=None):
        super()._combobox_selected_cb(event=event)


    #
    # Diğerleri
    #
    
    def _get_icon_paths(self, icon_name:str):
        def_icon_path = [
            self.ICONS_DIR,
            "playlist",
            f"{icon_name}.png"
        ]
        hover_icon_path = [
            self.ICONS_DIR,
            "playlist",
            f"{icon_name}(hover).png"
        ]

        return (def_icon_path, hover_icon_path)
    