import tkinter as tk
from tkinter import Misc, ttk
import tkinter.font as tkFont
import customtkinter as ctk

from tools import Event, EventWithArgs

from .page import Page
from .song_table import SongTable

class MainPage(Page):
    def __init__(self, root:Misc):
        super().__init__(root)

        # Fields
        self.button_font = tkFont.Font(family="Helvetica", size=14)

        # Events
        self.go_back_button_clicked = Event()
        self.queue_ch:EventWithArgs = EventWithArgs()
        self.setted_load:EventWithArgs = EventWithArgs()

        # Widgets
        self.listview_frame:ctk.CTkFrame
        self._frame:ctk.CTkFrame #Treeview'i kısıtlamak için kullandığımız dümenden frame
        self.song_table:SongTable
        self.x_scrollbar:ctk.CTkScrollbar
        self.y_scrollbar:ctk.CTkScrollbar

    def post_set(self):
        self.song_table.queue_changed = self.queue_ch
        self.song_table.double_clicked = self.setted_load

    def start(self):
        self.create_widgets()
        self.post_set()
        self.pack_widgets()
        self.styling()
        self.song_table._fill_treeview()
        
    #
    # Widget Oluşturma Metodları
    #

    def styling(self):
        style = ttk.Style(self.listview_frame)
        style.configure(
            "Treeview",
            background="#708090",  # arka plan rengi
            fieldbackground="#708090",  # alan arka plan rengi
            foreground="black",  # yazı rengi
        )

        styleh = ttk.Style(self.listview_frame)
        styleh.configure("Treeview.Heading",
                background="#36454F", # başlık arka plan rengi
                foreground="black",  # başlık yazı rengi
                font=('Calibri', 10, 'bold'))  # başlık fontu


    def create_widgets(self):
        self.create_listview_frame()

    def pack_widgets(self):
        pass

    def create_listview_frame(self):
        self.listview_frame = ctk.CTkFrame(self)
        self.listview_frame.pack()
        self.create_treeview(master=self.listview_frame)

        self.y_scrollbar = ctk.CTkScrollbar(
            self.listview_frame,
            orientation="vertical", 
            command=self.song_table.yview
        )
        self.y_scrollbar.pack(side="right",fill="y")
        self.song_table.configure(yscrollcommand=self.y_scrollbar.set)

        self.x_scrollbar = ctk.CTkScrollbar(
            self.listview_frame,
            orientation="horizontal",
            command=self.song_table.xview
        )
        self.x_scrollbar.pack(side="bottom",fill="x")
        self.song_table.configure(xscrollcommand=self.x_scrollbar.set)

        self.song_table.pack(side="left")
        self._frame.pack(side="left", fill="both", expand=True)


    def create_treeview(self, master=None):
        if master == None:
            master = self

        self._frame = ctk.CTkFrame(
            master=master,
            width=400,
            height=350
        )
        
        self._frame.propagate(False)

        self.song_table = SongTable(
            master=self._frame
        )

    def create_submenu_button(self, master, text:str, cb) -> tk.Button:
        _button = tk.Button(
            master, text=text,
            font=self.button_font,
            command=cb,
            width=14, height=3
            )
        return _button

    #
    # Treeview İçin Metodlar
    #


    #
    # Diğer Metodlar
    #


