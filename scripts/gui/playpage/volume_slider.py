import customtkinter as ctk
from tools import EventWithArgs

class VolumeSliderFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Events
        self.volume_ch = EventWithArgs()

        # Fields
        self.is_on_click = False
        self.current_volume = 0.0

        # Texts
        self.text_volume = "none text pp.volume_slider"

        # Widgets
        self.slider: ctk.CTkSlider
        self.volume_label: ctk.CTkLabel

    def start(self):
        self.create_widgets()
        self.pack_widgets()

        self.slider.bind("<Button-1>", self.__slider_on_click)
        self.slider.bind("<ButtonRelease-1>", self.__slider_on_release)
        self.slider.set(50.0)  # Default volume level

    def create_widgets(self) -> None:
        self.slider = ctk.CTkSlider(
            master=self,
            from_=0, to=100,
            orientation="horizontal",
            width=300,
            height=20
        )

        self.volume_label = ctk.CTkLabel(
            master=self,
            text=f"{self.text_volume}: 50%",
            padx=20
        )

    def pack_widgets(self):
        self.volume_label.pack(side="left", padx=10)
        self.slider.pack(side="left", pady=10)

    #
    #
    #

    def config_texts(self):
        self.volume_label.configure(
            text = self.text_volume 
        )


    def set_volume(self, volume: float):
        if not self.is_on_click:
            self.slider.set(volume)
            self.volume_label.configure(
                text=f"{self.text_volume}: {int(volume)}%"
            )

    #
    # Callbacks
    #

    def __slider_on_click(self, event):
        self.is_on_click = True

    def __slider_on_release(self, event):
        val = self.slider.get()
        self.volume_ch.sync_trigger(val)
        self.volume_label.configure(
            text=f"{self.text_volume}: {int(val)}%"
        )
        self.is_on_click = False
