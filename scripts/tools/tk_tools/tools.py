import tkinter as tk
from tkinter import Misc
from os.path import join
from PIL import Image
import customtkinter as ctk

def create_space(
        pady = 0,
        padx = 0,
        master:Misc = None,
    ) -> tk.Frame:
    """Boşluk oluşturucu\nBoş bir Frame oluşturup yerleştirir"""
    return tk.Frame(master,padx=padx, pady=pady)

def get_icon(*paths:str, scale:tuple = (1,1)) -> ctk.CTkImage:
    '''pathleri joinler'''
    return ctk.CTkImage(
        Image.open(join(
            *paths
        ))
    )
