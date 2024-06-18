import customtkinter as ctk
from tkinter import Misc
from os.path import join, exists
from PIL import Image, ImageEnhance
from typing import Literal

class IconButton(ctk.CTkButton):
    def __init__(
            self,
            master: Misc,
            def_icon_path: list[str] | str,
            hover: list[str] | Literal["darker", "lighter", "none"] | str,
            size: tuple = (20, 20),
            command=None
    ):
        ''' <hover> parametresine "darker", "lighter" veya başka bir resim için ise icon path girebilirsiniz(def_icon_path ile aynı şekilde)'''

        self.def_icon:ctk.CTkImage = None
        self.hover_icon:ctk.CTkImage = None

        self.flag:bool = False #^^^DEV^^^ şimdilik kondu ama bu event bağlamlarına ayar çekmek lazım aynı anda çok kez çağrıyorlar

        self.__icon_loading(
            def_icon_path,
            hover,
            size=size
        )



        super().__init__(
            master=master,
            text="",
            width=0,
            height=0,
            bg_color="transparent",
            fg_color="transparent",
            command=command,
            image=self.def_icon
        )

        self._event_binding()

    #
    # Şahsi
    #

    def config_icon(
        self,
        new_def_path: list[str] | str,
        new_hover: list[str] | str | Literal["darker", "lighter", "none"],
        size=(20, 20)
    ):
        ''' <hover> parametresine "darker", "lighter" veya başka bir resim için ise icon path girebilirsiniz(def_icon_path ile aynı şekilde)'''
        if self.flag: return

        self.flag = True
        self.__icon_loading(
            new_def_path,
            new_hover,
            size=size
        )

        self.configure(
            image=self.def_icon
        )

        self.flag = False

    def __icon_loading(
        self,
        def_path: list[str] | str,
        hover: list[str] | str | Literal["darker", "lighter", "none"],
        size=(20, 20)
    ):
        ''' <hover> parametresine "darker", "lighter" veya başka bir resim için ise icon path girebilirsiniz(def_icon_path ile aynı şekilde)'''

        if type(def_path) is not str:
            def_path = join(*def_path)

        dimg = Image.open(def_path)

        if type(hover) is not str:
            hover = join(*hover)

        match hover:
            case "darker":
                himg = ImageEnhance.Brightness(dimg).enhance(0.7)
            case "lighter":
                himg = ImageEnhance.Brightness(dimg).enhance(2.0)
            case "none":
                himg = dimg
            case _:  # path
                if not exists(hover):
                    hover = def_path
                himg = Image.open(hover)

        self.def_icon = ctk.CTkImage(dimg, size=size)
        self.hover_icon = ctk.CTkImage(himg, size=size)

    #
    # Event İşlemleri
    #

    def _event_binding(self):
        self.bind("<Leave>", self._on_leave)
        self.bind("<Enter>", self._on_enter)

    def _on_leave(self, event=None):
        self.configure(
            image=self.def_icon
        )


    def _on_enter(self, event=None):
        self.configure(
            image=self.hover_icon
        )