from types import FunctionType
import screeninfo
import pickle
import os

# Will get overwritten by init() (supress ide errors)
def update_taskbar(): ...
start_pinned = []
apps = set()
apps_dict = {}
app_ids = set()
class ui:
    def nothing(self,*args, **kwargs):
        """Does nothing"""

def init(g,l):
    globals().update(g)
    globals().update(l)

class Application:
    def __init__(
            self,
            id:str,
            name:str,
            version:int,
            onLaunch:FunctionType,
            onQuit:FunctionType=ui.nothing,
            iconPath:os.PathLike=''
        ):
        self.id = id
        self.name = name
        self.version = version
        self.onLaunch = onLaunch
        self.onQuit = onQuit
        self.windows = set()
        
        self.icon = iconPath
        
        self.pinned = False
        self.open = False

        for i in apps:
            if i.id == self.id:
                del self
                return

        apps.add(self)
        apps_dict[id] = self
        app_ids.add(self.id)

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
        try: self.onLaunch(self)
        except Exception as e: print(e)
        return self
    
    def quit(self):
        global taskbar_items
        for window in self.windows:
            if not window.quit_:
                window.quit()

        self.open = False
        if not self.pinned and self in taskbar_items:
            taskbar_items.remove(self)
        update_taskbar()
        try: self.onQuit(self)
        except: ...

class FileSystem:
    def __init__(self, path:str):
        self.path = path
        self.files = self.open(path)

    def open(self,path):
        if not os.path.exists(path):
            return {}

        with open(path, 'rb') as file:
            files = pickle.load(file)
        return files

    def close(self):
        with open(self.path, 'wb') as file:
            pickle.dump(self.files, file)

    def create(self, name:str):
        if not name.startswith('/'): name = f'/{name}'
        if name in self.files:
            raise FileExistsError(f"File '{name}' already exists!")

        self.files[name] = {
            'name': name.rsplit('/', 1)[1],
            'path': name,
            'data': b'',
            'size': 0,
        }

    def delete(self, name:str):
        if not name.startswith('/'): name = f'/{name}'
        if name not in self.files:
            raise FileNotFoundError(f"File '{name}' not found!")

        self.files.pop(name)
    
    def exists(self, name:str):
        return name in self.files

    def read(self, name:str):
        if not name.startswith('/'): name = f'/{name}'
        if name not in self.files:
            raise FileNotFoundError(f"File '{name}' not found!")

        return self.files[name]['data']

    def write(self, name:str, data:bytes):
        if not name.startswith('/'): name = f'/{name}'
        if name not in self.files:
            self.create(name)

        self.files[name]['name'] = name.rsplit('/', 1)[1]
        self.files[name]['path'] = name
        self.files[name]['data'] = data
        self.files[name]['size'] = len(data)

    def read_meta(self, name):
        if name not in self.files:
            raise FileNotFoundError(f"File '{name}' not found!")

        meta = self.files[name]
        meta.pop('data')

        return meta

    def write_meta(self, name, meta):
        if name not in self.files:
            self.create(name)

        self.files[name].update(meta)

    def dir_contains(self, file:str, dir:str):
        dir = dir.removeprefix('/').removesuffix('/')
        return file.removeprefix('/').startswith(f'{dir}/')

    def listdir(self, dir:str):
        if dir == '.': dir = '/'

        return [file['name'] for file in self.files.values() if self.dir_contains(file['path'], dir)]


    def __enter__(self):
        self.open(self.path)
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

fs = FileSystem('fs.bin')

class fs_open:
    def __init__(self, file_name:str, mode:str='w', fs: FileSystem = fs):
        self.file_name = file_name
        self.mode = mode
        self.fs = fs
        if not fs.exists(file_name) and 'r' in mode:
            raise FileNotFoundError(f"File '{file_name}' not found!")

    def read(self, size: int = -1):
        return self.fs.read(self.file_name)

    def write(self, data: bytes):
        self.fs.write(self.file_name, data)

    def __enter__(self):
        fs.open(fs.path)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        fs.close()


size =  screeninfo.get_monitors()[0].width, screeninfo.get_monitors()[0].height
