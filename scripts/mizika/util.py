class MizikaError(Exception):
    base_text:str = "Raised an error on Mizika"
    
    def __init__(self, *args: object) -> None:
        text = "\n--> " + self.base_text + "\n::: Error is:"
        for arg in args:
            if isinstance(arg, Exception):
                for arg in arg.args:
                    text += " " + arg            
            else: 
                text += " " + arg
        
            text += "\n::"

        super().__init__(text)
        
class MizikaCoreError(MizikaError):
    base_text:str = "This error occurred in Mizika's core."

class MizikaCantReadFileError(MizikaError):
    base_text:str = "Mizika can't read this file"

class MizikaPlaylistError(MizikaError):
    base_text:str = "This error occurred in Mizika's playlist."

class MizikaPLListError(MizikaError):
    base_text:str = "This error occured in Mizika's playlist list (PLList)"

class MizikaManagerError(MizikaError):
    base_text:str = "This error occured in Mizika Manager"

def get_msg(e:Exception):
    text = ""
    for arg in e.args:
        text += arg
    return text 