import yt_dlp as youtube_dl
import os

def download_list(
    url:str,
    dir_path:str = None, 
    status_func=None,
    text_f="İndirme tamamlandı",
    text_d=[
        "İndiriliyor",
        "tamamlandı",
        "kaldı"
    ]
):
    def pass_func(d): pass

    def my_hook(d):
        if d['status'] == 'finished': status_func(f"{text_f}: {d['filename']}")  
            
        elif d['status'] == 'downloading': status_func(f"{text_d[0]}: {d['filename']}, {d['_percent_str']} {text_d[1]}, {d['_eta_str']} {text_d[2]}.")

    hook = pass_func if status_func is None else my_hook

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [hook],
        'verbose': True,
        'outtmpl': os.path.join(dir_path, '%(title)s.%(ext)s') if dir_path is not None else '%(title)s.%(ext)s',
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def wrapper_handler(dl_func) -> str:
    try: dl_func()
    except Exception as e: return e.args

if __name__ == "__main__":
    # İndirmek istediğin YouTube listesinin  URL'si
    playlist_url = 'https://www.youtube.com/playlist?list=PL7RoFjquJ67Rvfi4z-0u7ducW1D-Rs8c9'  
    download_list(
        playlist_url, 
        dir_path = "/home/ustad/Projects/Python/Muzika 9/scripts/utube/playlists/jojo",
        status_func = None,
        text_f = "Download Success",
        text_d= [
            "Downloading",
            "done",
            "left"
        ]
    )