from tools import Event
from tools.tk_tools import IconButton
from gui.temps import Header

class PPHeader(Header):
    def __init__(self, master, icons_dir):
        super().__init__(master, icons_dir=icons_dir)

        #Events
        self.edit_button_clicked:Event = self._left_header_button_clicked
        
        #Fields
        self.text_page_title = "none text pp.header"

        #Widgets
        self.edit_button:IconButton = self._left_header_button

    def config_texts(self):
        super().config_texts()

    def start(self):
        super().start()
        self.edit_button = self._left_header_button
        self.edit_button.config_icon(
            new_def_path=[self.ICONS_DIR, "navigation", "edit.png"],
            new_hover="darker",
            size=(30,30)
        )

