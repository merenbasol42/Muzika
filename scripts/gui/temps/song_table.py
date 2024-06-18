from tkinter import ttk, Misc
import tkinter.font as tkFont
from typing import Literal, List
from tools import EventWithArgs

class SongTable(ttk.Treeview):
    EDIT_MODE: chr = 'e'
    PLAY_MODE: chr = 'p'

    def __init__(self, master: Misc):
        super().__init__(
            master,
            height=20,
            show="headings",
            columns=("id", "song")
        )

        self.queue_changed: EventWithArgs = EventWithArgs()
        self.double_clicked: EventWithArgs = EventWithArgs()

        self.MIN_COLUMN_SIZE: int = 370
        self.text_song_column: str = "none text song column table"
        self.table_list: List[str] = ["example_1.mp3", "example_2.mp3", "example_3.mp3"]

        self.heading("id", text="ID")
        self.heading("song", text=self.text_song_column)
        self.column("id", width=30)
        self.column("song", width=self.MIN_COLUMN_SIZE, anchor="center")

        self.column("song", width=700)

        self.filling_flag = False
        self.dragged_item = None
        self.initial_index = None

        self.click_flag = False

    #
    # Şahsi
    #

    def set_table_list(self, str_list: List[str]) -> None:
        if not str_list: str_list = []
        self.table_list = str_list
        self._fill_treeview()

    def set_column_name(self, new_name: str) -> None:
        self.heading("song", text=new_name)

    def _fill_treeview(self) -> None:
        if self.filling_flag or self.table_list is None:
            return

        self.filling_flag = True
        self._clear_treeview()
        self._insert_items()
        self.filling_flag = False
        self._adjust_column_size()

    def _clear_treeview(self) -> None:
        """Treeview'deki önceki öğeleri siler."""
        [self.delete(item) for item in self.get_children()]

    def _insert_items(self) -> None:
        """Verileri Treeview'e ekler."""
        for item in enumerate(self.table_list):
            self.insert("", "end", values=item)

    def _adjust_column_size(self) -> None:
        """Kolon genişliğini içeriklere göre ayarlar."""
        self.pack_forget()
        width = tkFont.Font().measure(self._get_most_length_in_list("A"))
        width = max(width, self.MIN_COLUMN_SIZE)
        self.column("song", width=width)
        self.pack(side="left")

    def _get_most_length_in_list(self, default_value: str = "A") -> str:
        if not self.table_list:
            return default_value

        return max(self.table_list, key=len)

    def get_treeview_items(self, item: str = "") -> List[str]:
        """Treeview'deki öğelerin 'values' özelliğini alır ve bir liste olarak döndürür."""
        items_list = []
        for child in self.get_children(item):
            item_values = self.item(child, 'values')
            items_list.append(item_values[1])
        return items_list

    #
    # Event Metodları
    #

    def event_bind(self, keyword: Literal["queue", "double_click", "selection"]) -> None:
        match keyword:
            case "queue":
                self._bind_queue_events()
            case "double_click":
                self._bind_double_click_event()
            case "selection":
                self._bind_selection_event()
            case _:
                raise ValueError("Invalid event keyword")

    def _bind_queue_events(self) -> None:
        self.bind('<Button-1>', self._on_drag_start)
        self.bind('<B1-Motion>', self._on_drag_motion)
        self.bind('<ButtonRelease-1>', self._on_drag_release)

    def _bind_double_click_event(self) -> None:
        self.bind("<Double-1>", self._on_double_click)

    def _bind_selection_event(self) -> None:
        self.config(selectmode="none")
        self.bind('<Button-1>', self._on_click_selection)
        self.click_flag = True

    def event_unbind(self, keyword: Literal["queue", "double_click", "selection"]) -> None:
        match keyword:
            case "queue":
                self._unbind_queue_events()
            case "double_click":
                self._unbind_double_click_event()
            case "selection":
                self._unbind_selection_event()
            case _:
                raise ValueError("Invalid event keyword")

    def _unbind_queue_events(self) -> None:
        self.unbind('<Button-1>')
        self.unbind('<B1-Motion>')
        self.unbind('<ButtonRelease-1>')

    def _unbind_double_click_event(self) -> None:
        self.unbind("<Double-1>")

    def _unbind_selection_event(self) -> None:
        self.config(selectmode="browse")
        self.unbind('<Button-1>')

    def _on_drag_start(self, event) -> None:
        """Sürüklemeye başlama olayı."""
        item = self.identify('item', event.x, event.y)
        if item:
            self.dragged_item = item
            self.initial_index = self.index(item)

    def _on_drag_motion(self, event) -> None:
        """Sürüklenen öğenin üzerine gelindiğinde."""
        item = self.identify('item', event.x, event.y)
        if item and item != self.dragged_item:
            self.move(self.dragged_item, self.parent(item), self.index(item))

    def _on_drag_release(self, event) -> None:
        """Sürüklemeyi bırakma olayı."""
        if self.dragged_item:
            self._sorted_cb()
        self.dragged_item = None

    def _sorted_cb(self) -> None:
        sorted_list = self.get_treeview_items()
        final_index = self.index(self.dragged_item)

        if final_index is not None:
            self.set_table_list(sorted_list)
            self.queue_changed.sync_trigger(self.initial_index, final_index)

    def _on_double_click(self, event) -> None:
        item = self.identify('item', event.x, event.y)
        index = int(self.index(item))
        self.double_clicked.sync_trigger(index)

    def _on_click_selection(self, event=None) -> None:
        if self.click_flag:
            item = self.identify_row(event.y)
            current_selection = self.selection()

            if item in current_selection:
                self.selection_remove(item)
            else:
                self.selection_add(item)
