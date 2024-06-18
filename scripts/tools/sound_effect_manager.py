import playsound as ps
from os.path import join 

class SEManager:
    '''
        Sound Effect Manager
    '''
    def __init__(self, sound_dir:str) -> None:
        self.sound_dir:str = sound_dir

    def play(self, name:str):
        full_path = join(
            self.sound_dir,
            name
        )
        ps.playsound(full_path)