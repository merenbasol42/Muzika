import customtkinter as ctk
import tkinter as tk
from threading import Thread

from tools import Event, EventWithArgs
from tools.tk_tools import ask_str_by_combox, ask_two_strings


class ControlFrame(ctk.CTkFrame):
    
    CHOOSE_MODE:int = 1
    QUEUE_MODE:int = 2

    def __init__(self, master, wn):
        super().__init__(master)

        # Events
        self.add_button_clicked:EventWithArgs = EventWithArgs()
        self.inner_remove_button_clicked:EventWithArgs = EventWithArgs()
        self.utube_input_given:EventWithArgs = EventWithArgs()
        
        self.radio_button_choosen:Event = Event()

        # Consts
        self.DEF_TEXT:str = "none text ep.cf"
        self.WN = wn

        # Fields
        self.radio_var = tk.IntVar(value=0)

        # Texts
        self.text_add_inp:str = self.DEF_TEXT 
        self.text_add_inp_title:str = self.DEF_TEXT    
        
        self.text_utube_inp_pl:str = self.DEF_TEXT
        self.text_utube_inp_url:str = self.DEF_TEXT
        self.text_utube_inp_button:str = self.DEF_TEXT
        self.text_utube_inp_title:str = self.DEF_TEXT

        self.text_add_button:str = self.DEF_TEXT
        self.text_remove_button:str = self.DEF_TEXT
        self.text_utube_button:str = self.DEF_TEXT

        self.text_choose_rb:str = self.DEF_TEXT
        self.text_queue_rb:str = self.DEF_TEXT

        self.text_choice_dir:str = "dir"
        self.text_choice_file:str = "file"

        # Widgets
        self.radio_buttons_frame:ctk.CTkFrame
        self.choose_rb:ctk.CTkRadioButton
        self.queue_rb:ctk.CTkRadioButton

        self.row0:ctk.CTkFrame
        self.add_button:ctk.CTkButton
        self.remove_button:ctk.CTkButton
        self.utube_button:ctk.CTkButton

    def start(self):
        self.create_widgets()
        self.pack_widgets()
        self.radio_var.set(
            ControlFrame.CHOOSE_MODE
        )
        self._radio_button_cb()
        self.config_texts()

    def create_widgets(self):
        self.row0 = ctk.CTkFrame(self)
        
        self.add_button = self.create_edit_button(
            master=self.row0, text=self.text_add_button, cb=self.add_button_cb
        )
        self.remove_button = self.create_edit_button(
            master=self.row0, text=self.text_remove_button, cb=self._remove_button_cb
        )
        self.utube_button = self.create_edit_button(
            master=self.row0, text=self.text_utube_button, cb=self._utube_button_cb
        )

        # Radio Buttons Frame
        self.radio_buttons_frame = ctk.CTkFrame(
            self
        )
        self.choose_rb = self.create_rb(
            value=ControlFrame.CHOOSE_MODE, text=self.text_choose_rb
        )
        self.queue_rb = self.create_rb(
            value=ControlFrame.QUEUE_MODE, text=self.text_queue_rb
        )

    def pack_widgets(self):
        self.add_button.pack(side="left", padx=10)
        self.remove_button.pack(side="right", padx=10)
        self.utube_button.pack(expand=False, padx=10)
        self.row0.pack(side="bottom", fill="x", pady=(10,50))

        self.choose_rb.pack(side="left", padx=10)
        self.queue_rb.pack(side="right", padx=10)
        self.radio_buttons_frame.pack(side="bottom", fill='x', pady=(20,20), padx=(20,20))

    def create_rb(self, value:int, master=None, cb=None, text:str="", var:tk.IntVar=None ) -> ctk.CTkRadioButton:
        
        if master is None:
            master = self.radio_buttons_frame
        if cb is None:
            cb = self._radio_button_cb
        if var is None:
            var = self.radio_var

        return ctk.CTkRadioButton(
            master=master,
            text=text,
            variable=var,
            value=value,
            command=cb
        )

    def create_edit_button(self, master=None, cb=None, text:str=""):
        if cb is None:
            cb = self.pass_func
        if master is None:
            master = self

        return ctk.CTkButton(
            master,
            text=text,
            width=100,
            height=40,
            command=cb
        )
    
    #
    # Callbacks
    #

    def add_button_cb(self):

        def func():
            ask_str_by_combox(
                result_cb=self.__add_button_cb_s2,
                parent=self.WN,
                inp_title=self.text_add_inp_title,
                inp_text=self.text_add_inp,
                combox_list=[
                    self.text_choice_dir,
                    self.text_choice_file
                ],
            )
        
        # aga çalıştıran thread yorulmasın kendimizinkini çalıştıralım
        # Çok bekleyebiliir 
        Thread(target=func).start()

    def __add_button_cb_s2(self, result):
        if result is None: return
        
        paths = []
        match result:
            case self.text_choice_dir:    paths.append(ctk.filedialog.askdirectory())
            case self.text_choice_file:    paths = ctk.filedialog.askopenfilenames()
            case x:    raise Exception(f"Hayad bitti <<{x}>> diye bi şi yok caselerde")

        self.add_button_clicked.sync_trigger(*paths)

    def _remove_button_cb(self):
        self.inner_remove_button_clicked.sync_trigger()

    def _utube_button_cb(self):
        def func():
            inp:list[str] | tuple[None] = ask_two_strings(
                parent = self.WN,
                toplevel_title = self.text_utube_inp_title,
                first_inp_text = self.text_utube_inp_pl,
                second_inp_text = self.text_utube_inp_url,
                button_name = self.text_utube_inp_button 
            )
            
            if inp is not None: self.utube_input_given.sync_trigger(*inp) 
        
        # aga çalıştıran thread yorulmasın kendimizinkini çalıştıralım
        # Çok bekleyebiliir 
        Thread(target=func).start()

    def __utube_button_cb_s2(self, result):
        if result is None: return
        
        paths = []
        match result:
            case self.text_choice_dir:    paths.append(ctk.filedialog.askdirectory())
            case self.text_choice_file:    paths = ctk.filedialog.askopenfilenames()
            case x:    raise Exception(f"Hayad bitti <<{x}>> diye bi şi yok caselerde")

        self.add_button_clicked.sync_trigger(*paths)

    def _radio_button_cb(self):
        self.radio_button_choosen.sync_trigger()

    #
    # Diğerleri
    #

    def config_texts(self):
        """metinsel ifadelerdeki değişikliklerin widgetlara yansımması\niçin konfigüre edilmesini sağlar"""
        # add inp ile add inp title' ı configüre etmeye gerek yok
        # utube_inp textlerini configüre etmeye gerek yok
        self.add_button.configure(
            text=self.text_add_button
        )
        self.remove_button.configure(
            text=self.text_remove_button
        )
        self.utube_button.configure(
            text=self.text_utube_button
        )
        self.choose_rb.configure(
            text=self.text_choose_rb
        )
        self.queue_rb.configure(
            text=self.text_queue_rb
        )
        # choice dir ile choice file'ı da konfigüre etmeye gerek yok
        
    def pass_func():
        pass