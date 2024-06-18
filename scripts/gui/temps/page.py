import customtkinter as ctk
from tkinter import Misc

class Page(ctk.CTkFrame):
    def __init__(self, master:Misc):
        super().__init__(master=master)
        self.master = master

    def start(self):
        pass

    def display(self):
        self.pack(fill="both", expand=True)
    
    def undisplay(self):
        self.pack_forget()

    def config_texts(self):
        pass