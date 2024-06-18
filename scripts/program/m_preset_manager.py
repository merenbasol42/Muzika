import json
from os.path import exists

class MPresetManager:
    # Muzika Preset Manager
    def __init__(self, file_path:str) -> None:
        if not exists(file_path):
            raise Exception("Preset file is not exist") 
        self.file_path:str = file_path
        self.lang_code:str = None

    def load(self):
        content:dict = {}
        with open(self.file_path, 'r') as f:
            content:dict = json.loads(f.read())
        
        self.lang_code = content["lang"]
        
    def save(self):
        content:dict = {}
        content["lang"] = self.lang_code

        with open(self.file_path, 'w') as f:
            f.write(json.dumps(content,indent=4))