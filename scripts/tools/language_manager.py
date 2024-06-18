import json
import os

class LanguageManager:
    def __init__(self, path:str) -> None:
        if not os.path.exists(path):
            raise Exception(f"Aganiga dil dosyası yok <language_dir> is not exist {path}")
        
        self.path:str = path
        self.langs:list[Language] = []

    def load_langs(self):
        for dir_name in os.listdir(self.path):
            dir_path = os.path.join(self.path, dir_name)
            
            if os.path.isdir(dir_path):
                self.langs.append(
                    Language(
                        path=dir_path
                    )
                )

class Language:
    def __init__(self, path:str, name = None):

        if not os.path.exists(path):
            raise Exception(f"Aganiga dil dosyası yok <path> is not exist \nError in <Language> class\n{path}")
        
        self.path:str = path

        if name is None:
            name = os.path.splitext(
                os.path.basename(
                   path 
                )
            )[0]
        
        self.code:str = name 
        
        self.docs_path:dict[str][str] = {}

    def load(self):
        self.docs_path.clear()
        for doc_name in os.listdir(self.path):
            doc_path = os.path.join(self.path, doc_name)
            self.add_doc(doc_path)

    def add_doc(self, path:str):
        key = os.path.splitext(
            os.path.basename(
                path 
            )
        )[0]
        self.docs_path[key] = path

    def get_content(self, doc_key:str) -> dict:
        doc_path = self.docs_path[doc_key]

        _dict = {}
        with open(doc_path, 'r') as f:
            _dict = json.loads(
                f.read()
            )

        return _dict


