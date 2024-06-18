from tkinter import Tk, Frame
from typing import Literal

class RowNavigator:
    def __init__(self, root:Tk) -> None:
        self.root = root
        self.__x0 = None
        self.__y0 = None
        self.__xc = None
        self.__xt = None
        self.__time = None
        self.__start_vel = None

    def first_page_show(self, page:Frame):
        page.pack(fill="both", expand=True)

        def mainloop_after():
            page.configure(
                width = page.winfo_width(),
                height = page.winfo_height() 
            )
            page.propagate(False)
            x = page.winfo_x()
            y = page.winfo_y()
            page.pack_forget()
            page.place(x=x, y=y)


        self.root.after(100, mainloop_after)

    def pass_page(self ,current_page:Frame, target_page:Frame, from_:Literal["left", "right"]):
        match from_:
            case "left":
                self.__pass_page(current_page, target_page, -1)
            case "right":
                self.__pass_page(current_page, target_page, 1)
            case x:
                raise Exception(f"{x} is not a valid value. Only 'left' and 'right' are acceptable")


    def __pass_page(self, current_page:Frame, target_page:Frame, dir_:int):
        """dir=1 -> from right, dir=-1, from left """
        target_page.configure(
            width = current_page.winfo_width(),
            height = current_page.winfo_height() 
        )

        pwidth = current_page.master.winfo_width()
        target_page.propagate(False)
        self.__start_vel = pwidth/8
        self.__x0 = current_page.winfo_x()
        self.__y0 = current_page.winfo_y()
        self.__xc = 0 
        self.__xt = dir_*pwidth
        self.__time = 0 

        target_page.place(x=self.__xt, y=self.__y0)

        def recursive():
            vel = dir_*self.calc_vel()
            
            self.__xc -= vel
            self.__xt -= vel
            
            current_page.place(
                x=self.__xc,
                y=self.__y0
            )
            target_page.place(
                x=self.__xt,
                y=self.__y0
            )

            if not dir_*self.__xt < 0:
                self.root.after(10, recursive)
                self.__time += 1
            else:
                target_page.place(x=self.__x0, y=self.__y0) # tam 0,0 noktasına denk gelmemiş olabilir
                current_page.place_forget()

        recursive()


    def calc_vel(self) -> int:
        divider = 1 + self.__time*0.35
        calc = self.__start_vel/divider + 1
        return calc