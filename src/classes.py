import screeninfo
from os import PathLike
from types import FunctionType

# Will get overwritten by init() (supress ide errors)
def update_taskbar(): ...
start_pinned = []
apps = []

def init(g,l):
    globals().update(g)
    globals().update(l)

class Application:
    def __init__(self,id:str,name:str,onLaunch:FunctionType,onQuit:FunctionType,iconPath:PathLike='',always_call=False):
        self.id = id
        self.name = name
        self.onLaunch = onLaunch
        self.onQuit = onQuit
        self.window = None
        
        self.icon = iconPath
        
        self.pinned = False
        self.open = False

        apps.append(self)
    
    def pin(self,add_to_taskbar=True,add_to_start=True):
        if add_to_start: start_pinned.append(self)
        if add_to_taskbar:
            taskbar_items.append(self)
            self.pinned = True
        update_taskbar()
        return self
    
    def launch(self):
        if self.open:
            self.quit()
            return
        self.open = True
        if not self.pinned:
            taskbar_items.append(self)
        update_taskbar()
        self.onLaunch(self)
        return self
    
    def quit(self):
        global taskbar_items
        if self.window:
            if not self.window.quit_:
                self.window.quit()
        self.open = False
        if not self.pinned and self in taskbar_items:
            taskbar_items.remove(self)
        update_taskbar()
        self.onQuit(self)

size =  screeninfo.get_monitors()[0].width, screeninfo.get_monitors()[0].height
