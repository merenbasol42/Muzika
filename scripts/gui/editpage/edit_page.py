from tkinter import Misc

from tools import Event, EventWithArgs
from gui.temps import MainPage
from .ep_header import EPHeader
from .control_frame import ControlFrame


class EditPage(MainPage):

    def __init__(self, root: Misc, icons_dir, wn):
        super().__init__(root)

        # 
        self.DEF_TEXT:str = "none text ep.ep"
        self.text_song_column:str = self.DEF_TEXT

        # Organların Oluşturumu
        self._HEADER:EPHeader = EPHeader(self, icons_dir)
        self._CONTROL_FRAME:ControlFrame = ControlFrame(self, wn)
    
        self.remove_button_clicked:EventWithArgs = EventWithArgs()

        self.event_shell() #Organların eventlerine kabukluk ediliyor

        self.radio_button_choosen.subscribe(
            self._rb_choosen_cb
        )
        self._CONTROL_FRAME.inner_remove_button_clicked.subscribe(
            self._remove_button_clicked_cb
        )

    def start(self):
        self._HEADER.start()
        self._HEADER.pack(side="top", fill='x', pady=(0,10))
        
        self._CONTROL_FRAME.start()
        self._CONTROL_FRAME.pack(side="bottom", fill='x', padx=(10,10), pady=(10,10))

        super().start()
        self.text_shell() #Organların textlerine kabukluk ediliyor

    def config_texts(self):
        self._HEADER.config_texts()
        self._CONTROL_FRAME.config_texts()
        self.song_table.set_column_name(self.text_song_column)

    def event_shell(self):
        # Header'ın Eventleri
        self.play_page_button_clicked:Event = self._HEADER.go_back_button_clicked
        self.delete_pl_button_ck:Event = self._HEADER.delete_pl_button_clicked
        self.combobox_select:EventWithArgs = self._HEADER.combox_selected
        self.create_pl_button_ck:EventWithArgs = self._HEADER.create_pl_button_clicked
        self.settings_button_clicked:Event = self._HEADER.settings_button_clicked

        # Edit Button Frame'in Eventleri
        self.add_button_clicked:EventWithArgs = self._CONTROL_FRAME.add_button_clicked
        # self.remove_button_clicked EditPage tarafından sağlanmakta
        self.utube_button_clicked:EventWithArgs = self._CONTROL_FRAME.utube_input_given
        self.radio_button_choosen:Event = self._CONTROL_FRAME.radio_button_choosen

    def text_shell(self):
        # Header
        self.text_page_title:str = self._HEADER.text_page_title
        self.text_combobox_default:str = self._HEADER.text_pl_combox_default
        self.text_combobox_nothing:str = self._HEADER.text_pl_combox_nothing
        self.text_create_inp:str = self._HEADER.text_create_inp
        self.text_create_inp_title:str = self._HEADER.text_create_inp_title

        # Table
        self.text_song_column:str = self.song_table.text_song_column

        # Control Frame
        self.text_add_button:str = self._CONTROL_FRAME.text_add_button
        self.text_remove_button:str = self._CONTROL_FRAME.text_remove_button
        self.text_utube_button:str = self._CONTROL_FRAME.text_utube_button
        self.text_choose_rb:str = self._CONTROL_FRAME.text_choose_rb
        self.text_queue_rb:str = self._CONTROL_FRAME.text_queue_rb

        self.text_add_inp_title:str = self._CONTROL_FRAME.text_add_inp_title
        self.text_add_inp:str = self._CONTROL_FRAME.text_add_inp

        self.text_choice_dir:str = self._CONTROL_FRAME.text_choice_dir
        self.text_choice_file:str = self._CONTROL_FRAME.text_choice_file

    # (Kabuk Operasyonu)
    # Header Metodları (Sadece Dışarıdan Kullanılanlar) 
    #
    
    def set_pl_list(self, _list:list[str]):
        self._HEADER.set_pl_list(_list)

    ###

    def _rb_choosen_cb(self):
        val = self._CONTROL_FRAME.radio_var.get()

        match val:
            case ControlFrame.CHOOSE_MODE:
                self.song_table.event_unbind("queue")
                self.song_table.event_bind("selection")
            case ControlFrame.QUEUE_MODE:
                self.song_table.event_unbind("selection")
                self.song_table.event_bind("queue")
            case _:
                raise Exception("Aga başka mod mu varrr")
            
    def _remove_button_clicked_cb(self, event=None):
        indexs:list[int] = []
        for i in self.song_table.selection():
            values = self.song_table.item(i, "values")
            indexs.append(
                int(values[0])
            )
        self.remove_button_clicked.sync_trigger(*indexs)