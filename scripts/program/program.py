from os import path
from os import pardir
from typing import Literal

from tools import SEManager
from tools.funcs import get_file_paths_in_dir

from mizika import MizikaManager
from gui import GUI 
from utube import MuzikaListDownloader as MLD

from .m_preset_manager import MPresetManager
from .m_language_manager import MLanguageManager


class Program:
    
    def __init__(self, running_dir:str) -> None:
        # Constants
        if running_dir is None: # bu dosyanın bulunduğu yer olsun
            running_dir = path.join(path.dirname(path.abspath(__file__)), pardir)
        self.RUNNING_DIR:str = running_dir

        self.exit_flag:bool = False

        self.gui = GUI(
            icons_dir = path.join(
                self.RUNNING_DIR, 
                "assets", 
                "icons"
            )
        )

        self.MM = MizikaManager(
            self.RUNNING_DIR
        )

        self.mld = MLD(
            self.gui.root,
            self.RUNNING_DIR
        )

        
        self.mlm = MLanguageManager(
            path = path.join(
                self.RUNNING_DIR,
                "config",
                "languages"
            ),
            gui = self.gui,
            mld = self.mld 
        )

        self.sem = SEManager(
            sound_dir= path.join(
                self.RUNNING_DIR,
                "assets",
                "sounds"
            )
        )

        self.mpsm = MPresetManager(
            file_path=path.join(
                self.RUNNING_DIR,
                "config",
                "presettings.json"
            )
        )


        self.preset()

    #
    # Şahsi
    #

    def preset(self):
        self._bind_all_events()
        self.mlm.load_langs()
        self.mpsm.load()

    def postset(self):
        self.gui.popup_menu.sp.set_lang_list(
            [lang.code for lang in self.mlm.langs]
        )

        self.load_lang(
            self.mpsm.lang_code
        )

        self.MM.pl_list.load()
        self.MM.MIZIKA.start()
    
    def start(self):
        self.gui.start()
        self.postset() # postset burada çünkü bunu çalıştıran thread mainloopa düşmeden bunu yapması lazım. Mainloop programın sonuna kadar devam ediyor çünkü
        self.gui.root.mainloop()

    #
    # Event Bindings
    #

    def _bind_all_events(self):
        self._mizika_binding()
        self._bind_gui_events()

    def _mizika_binding(self):
        self.MM.pl_list.content_ch.subscribe(
            self.get_mm_cb("pl_list_c")
        )
        self.MM.edit_pl_ch.subscribe(
            self.get_mm_cb("edit_pl")
        )
        self.MM.edit_pl_content_ch.subscribe(
            self.get_mm_cb("edit_pl_c")
        )
        self.MM.play_pl_ch.subscribe(
            self.get_mm_cb("play_pl")
        )
        self.MM.play_pl_content_ch.subscribe(
            self.get_mm_cb("play_pl_c")
        )
        self.MM.MIZIKA.song_ch.subscribe(
            self.get_mm_cb("song")
        )
        self.MM.MIZIKA.mode_ch.subscribe(
            self.get_mm_cb("mode")
        )
        self.MM.MIZIKA.pause_ch.subscribe(
            self.get_mm_cb("pause")
        )
        self.MM.MIZIKA.pos_ch.subscribe(
            self.get_mm_cb("pos")
        )

    def _bind_gui_events(self):
        def quit_f():
            self.do_exit_works()
            self.MM.MIZIKA.stop()

        self.gui.quited.subscribe(quit_f)
        self._bind_gui_pp_events()
        self._bind_gui_ep_events()
        self._bind_gui_pm_events()
        
    def _bind_gui_pp_events(self):
        
        # Header
        self.gui.pp.combox_selected.subscribe(
            self.get_gui_pp_cb("combobox")
        )

        # Table
        self.gui.pp.setted_load.subscribe(
            self.get_gui_pp_cb("load")
        )
        self.gui.pp.queue_ch.subscribe(
            self.get_gui_pp_cb("queue")
        )

        # Trackbar
        self.gui.pp.pos_track_setted.subscribe(
            self.get_gui_pp_cb("pos")
        )

        # Volume
        self.gui.pp.volume_ch.subscribe(
            self.get_gui_pp_cb("volume")
        )

        # MediaPlayer
        self.gui.pp.prev_button_ck.subscribe(
            self.get_gui_pp_cb("previous")
        )
        self.gui.pp.rewind_button_ck.subscribe(
            self.get_gui_pp_cb("rewind")
        )
        self.gui.pp.play_button_ck.subscribe(
            self.get_gui_pp_cb("play")
        )
        self.gui.pp.forward_button_ck.subscribe(
            self.get_gui_pp_cb("forward")
        )
        self.gui.pp.next_button_ck.subscribe(
            self.get_gui_pp_cb("next")
        )

        # Controller
        self.gui.pp.mode_button_ck.subscribe(
            self.get_gui_pp_cb("mode")
        )
        self.gui.pp.load_button_ck.subscribe(
            self.get_gui_pp_cb("load")
        )

    def _bind_gui_ep_events(self):
        #Header
        # goback buttonın işi burası değil gui main
        self.gui.ep.create_pl_button_ck.subscribe(
            self.get_gui_ep_cb("create")
        )
        self.gui.ep.combobox_select.subscribe(
            self.get_gui_ep_cb("combobox")
        )
        self.gui.ep.delete_pl_button_ck.subscribe(
            self.get_gui_ep_cb("delete")
        )
        
        # Table
        self.gui.ep.queue_ch.subscribe(
            self.get_gui_ep_cb("queue")
        )

        #Control
        self.gui.ep.add_button_clicked.subscribe(
            self.get_gui_ep_cb("add")
        )
        self.gui.ep.utube_button_clicked.subscribe(
            self.get_gui_ep_cb("utube")
        )
        self.gui.ep.remove_button_clicked.subscribe(
            self.get_gui_ep_cb("remove")
        )

    def _bind_gui_pm_events(self):
        self.gui.popup_menu.sp.combox_selected.subscribe(
            self.get_gui_pm_cb("lang")
        )
   
    #
    # Callbacks
    #

    def get_mm_cb(
        self,
        keyword:Literal[
            "pl_list_c",
            "edit_pl", "edit_pl_c", "play_pl", "play_pl_c",
            "song", "mode", "pause", "pos"
        ]
    ):
        
        def pl_list_c_f():
            pl_name_list = [pl.get_name() for pl in self.MM.pl_list.get_content()]
            self.gui.pp.set_pl_list(
                pl_name_list
            )
            self.gui.ep.set_pl_list(
                pl_name_list
            )

        def edit_pl_c_f(): #Değiştirildi
            self.gui.ep.song_table.set_table_list(
                self.MM.get_path_list("edit")
            )

        def edit_pl_f():
            import time
            time.sleep(0.05) # pllist'in content eventinden daha hızlı çalışırsa diye ufak bir direnç
            self.gui.ep._HEADER.set_combobox_index(
                self.MM.pl_list.index(
                    self.MM.edit_pl.get_name()
                )
            )
            edit_pl_c_f()
                
        def play_pl_c_f(): 
            # Zaten PP'deki comboboxtan gelecek değişim isteği o yüzden gidip onu set etmenin bi manası yok ^^^DEV^^^ aga bu yanlış bi anlayış bunu düzelt
            if self.MM.play_pl is None:
                self.gui.pp.song_table.set_table_list([])
                return
            
            self.gui.pp.song_table.set_table_list(
                [song.get_name() for song in self.MM.play_pl.get_content()]
            )

        def play_pl_f():
            play_pl_c_f()

        def song_f():
            length = 0
            name = None
            if self.MM.MIZIKA.get_song() is None:
                length = 0.0
            else:
                length = self.MM.MIZIKA.get_song().get_length()
                name = self.MM.MIZIKA.get_song().get_name()

            self.gui.pp._TRACKBAR.set_song_length(
                length
            )
            self.gui.sp.set_song_label(
                name
            )

        def mode_f():
            self.gui.sp.set_playing_mode(
                self.MM.MIZIKA.get_mode()
            )

        def pause_f():
            self.gui.pp.set_pause_state(
                self.MM.MIZIKA.get_pause_state()
            )
            self.gui.sp.set_pause_state(
                self.MM.MIZIKA.get_pause_state()
            )

        def pos_f():
            self.gui.pp._TRACKBAR.set_song_pos(
                self.MM.MIZIKA.get_pos()
            )
      
        match keyword:
            case "pl_list_c": return pl_list_c_f
            case "edit_pl": return edit_pl_f
            case "edit_pl_c": return edit_pl_c_f
            case "play_pl": return play_pl_f
            case "play_pl_c": return play_pl_c_f
            case "song": return song_f
            case "mode": return mode_f
            case "pause": return pause_f
            case "pos": return pos_f

    def get_gui_pp_cb(
            self,
            keyword:Literal[
                "combobox",
                "queue",
                "previous", "rewind", "play", "forward", "next",
                "mode", "load", "pos", "volume"
            ]
        ):

        def combobox_f(index):
            self.MM.set_play_pl(index)

        def queue_f(old_index, new_index):
            if self.MM.play_pl is None: return

            song = self.MM.play_pl.get_song(old_index)
            self.MM.play_pl.pop(old_index, trigger=False)
            self.MM.play_pl.insert(new_index, song)

        def previous_f():
            if self.MM.play_pl is None: return
            
            self.MM.MIZIKA.play_previous_song()

        def rewind_f():
            if self.MM.MIZIKA.get_song() is None: return 
            
            self.MM.MIZIKA.rewind(5)

        def play_f():
            if self.MM.play_pl is None: return
            
            self.MM.MIZIKA.pause_toggle()

        def forward_f():
            if self.MM.MIZIKA.get_song() is None:
                return
            self.MM.MIZIKA.fast_forward(5)

        def next_f():
            if self.MM.play_pl is None: return
            
            self.MM.MIZIKA.play_next_song()

        def mode_f():
            self.MM.MIZIKA.set_mode_iterative()

        def load_f(index):
            if self.MM.play_pl is None: return
            self.MM.MIZIKA.play_song(index, save=True)

        def pos_f(target_pos):
            if self.MM.MIZIKA.get_song() is None: return 
            self.MM.MIZIKA.set_pos(target_pos)

        def volume_f(target_vol):
            self.MM.MIZIKA.set_volume(target_vol)

        match keyword:
            case "combobox": return combobox_f
            case "queue": return queue_f
            case "previous": return previous_f
            case "rewind": return rewind_f
            case "play": return play_f
            case "forward": return forward_f
            case "next": return next_f
            case "mode": return mode_f
            case "load": return load_f
            case "pos": return pos_f
            case "volume": return volume_f
            case _: raise Exception("Aganiga o kadar literal koyduk")

    def get_gui_ep_cb(
            self,
            keyword:Literal[
                "create", "combobox", "delete",
                "queue",
                "add", "utube", "remove"
            ]
        ):

        def create_f(name):
            _index = self.MM.pl_list.get_length()
            print(_index)
            self.MM.pl_list.create(name)
            import time
            time.sleep(0.1)
            self.MM.set_edit_pl(_index) # 1 tane eklendiği için çıkarmaya gerek yok
            self.gui.ep._HEADER.set_combobox_index(_index)

        def combobox_f(index):
            self.MM.set_edit_pl(index)

        def delete_f():
            self.MM.pl_list.delete(
                obj = self.MM.edit_pl
            )

            if self.MM.edit_pl == self.MM.play_pl:
                self.MM.MIZIKA.set_pl(None) 

        def queue_f(*args):
            if self.MM.edit_pl is None: return

            old_index = args[0]
            new_index = args[1]
            song = self.MM.edit_pl.get_song(old_index)
            self.MM.edit_pl.pop(old_index)
            self.MM.edit_pl.insert(new_index, song)
          
        def add_f(*paths:str):
            if self.MM.edit_pl is None: return

            def from_file(*song_paths:str):
                self.MM.edit_pl.add(*song_paths, safe=True)

            def from_dir(dir_path:str):
                from_file(
                    *get_file_paths_in_dir(dir_path)
                ) 

            if path.isdir(paths[0]): from_dir(paths[0])
            else: from_file(*paths)

            self.MM.edit_pl.save()

        def utube_f(pl_name:str, url:str):
            print(f"pl_name: {pl_name}")
            print(f"url: {url}")
        
            if self.mld.download(pl_name, url):
                _index = self.MM.pl_list.get_length()
                try: self.MM.pl_list.create(pl_name)
                except Exception: pass
                _index = self.MM.pl_list.index(pl_name + ".json")
                self.MM.set_edit_pl(_index)
            else: return

            def from_file(*song_paths:str):
                self.MM.edit_pl.add(*song_paths, safe=True)

            def from_dir(dir_path:str):
                from_file(
                    *get_file_paths_in_dir(dir_path)
                ) 

            from_dir(
                path.join(self.RUNNING_DIR, "musics", pl_name)
            )
            self.MM.edit_pl.save()
            
        def remove_f(*indexs:int):
            if self.MM.edit_pl is None: return
            
            self.MM.edit_pl.pop(*indexs)

        match keyword: 
            case "create": return create_f
            case "combobox": return combobox_f
            case "delete": return delete_f
            case "queue": return queue_f
            case "add": return add_f
            case "utube": return utube_f
            case "remove": return remove_f
            case _: raise Exception("Aganiga o kadar literal koyduk")

    def get_gui_pm_cb(
        self,
        keyword:Literal["lang"]
    ):
        def lang(lang_code): 
            self.load_lang(lang_code)

        match keyword:
            case "lang": return lang
            case x: raise Exception(f"{x} is not a valid keyword for _return_gui_pm_cb")

    #
    # Diğerleri
    #

    def pass_func(self):
        pass

    def load_lang(self, lang_code:str):
        self.mlm.set_current_lang(lang_code)
        self.mlm.current_lang.load()
        self.mlm.apply()
        self.gui.config_texts()
        self.gui.popup_menu.sp.set_lang(lang_code)
        self.get_mm_cb("song")()

    def do_exit_works(self):
        if self.exit_flag: return
        else: self.exit_flag = True
        
        self.mpsm.lang_code = self.mlm.current_lang.code
        self.mpsm.save()
        # Kullanıcı hiç playlist yüklemeden uygulamayı kapatmış olabilir 
        self.MM.pl_list.save_all()