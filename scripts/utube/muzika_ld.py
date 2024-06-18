import os
import customtkinter as ctk
from threading import Thread

from .utube_ld import download_list, wrapper_handler
from yt_dlp.utils import DownloadError, ExtractorError

class MuzikaListDownloader:

    DEF_TEXT = "none text MLD"
    def __init__(self, wn:ctk.CTk, running_dir:str) -> None:
        self.WN = wn
        
        self.MUSICS_DIR:str = os.path.join(running_dir, "musics")
        if not os.path.exists(self.MUSICS_DIR): os.mkdir(self.MUSICS_DIR)
        
        self.text_toplevel_title:str = self.DEF_TEXT
        self.text_toplevel_info:str = self.DEF_TEXT
        self.text_finished:str = self.DEF_TEXT
        self.texts_downloading:list[str] = [self.DEF_TEXT, self.DEF_TEXT, self.DEF_TEXT]

        self.text_error_download:str = self.DEF_TEXT
        self.text_error_success:str = self.DEF_TEXT
        self.text_error_input:str = self.DEF_TEXT

        #Toplevel
        self.top:ctk.CTkToplevel = None
        self.stat_label:ctk.CTkLabel = None 


    def download(self, pl_name:str, url:str):
        _pl_dir:str = os.path.join(self.MUSICS_DIR, pl_name)
        if not os.path.exists(_pl_dir): os.mkdir(_pl_dir) 
        # Eğer hali hazırda mevcut ise de onun içine indiririz
        
        Thread(target=self.__start_toplevel).start()
        try: 
            download_list(
                url=url,
                dir_path=_pl_dir,
                status_func=self.__status_func,
                text_f=self.text_finished,
                text_d=self.texts_downloading
            )
            self.__stop_toplevel(self.text_error_success)
            return True
        except DownloadError as e:
            if 'is not a valid URL' in str(e):
                self.__stop_toplevel(self.text_error_input)
                print(f"url error")
            else:
                self.__stop_toplevel(self.text_error_download)
                print("download error")
        
        except Exception as e:
            self.__stop_toplevel("Beklenmeyen bir hata oluştu.")
            print(f"Exception: {e}, Type: {type(e)}")

        return False

    def __status_func(self, text:str):
        self.stat_label.configure(
            text = text
        )

    def __start_toplevel(self):
        self.top = ctk.CTkToplevel(self.WN)
        self.top.geometry("250x250")
        self.top.title(self.text_toplevel_title)

        self.info_label = ctk.CTkLabel(self.top, text=self.text_toplevel_info)
        self.sc_frame = ctk.CTkScrollableFrame(self.top)
        self.stat_label = ctk.CTkLabel(
            self.sc_frame, text="...", wraplength=200
        )

        self.info_label.pack()
        self.stat_label.pack()
        self.sc_frame.pack(fill="both", expand=True)

        self.top.protocol("WM_DELETE_WINDOW", lambda: None) # kapatılmasın pencere

        self.top.wait_window()

    def __stop_toplevel(self, text):
        button = ctk.CTkButton(
            self.top, text="OK", command=self.top.destroy
        )

        self.sc_frame.pack_forget()
        button.pack(side="bottom", pady=10)
        self.info_label.pack_forget()
        self.sc_frame.pack()
        self.stat_label.configure(
            text = text
        )
        




