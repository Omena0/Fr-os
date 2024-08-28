from classes import Application, size
import engine as ui
from copy import copy

def open_app(app:Application):
    global fs,w

    x = size[0] // 2 - size[0]//3
    y = size[1] // 2 - size[1]//3
    w = ui.Window(
        position = (x,y),
        width=200,
        height=100,
        title=app.name
    ).add(ui.root)
    app.window = w
    app.windows.add(w)
    w.buttons = []

    update_dir(app,'/')

def update_dir(app,d:str):
    global w, dir

    dir = d

    print(dir)

    for i in w.buttons:
        try:
            w.remove(i)
        except: ...

    w.buttons = []

    with fs:
        dirlist = fs.listdir(dir)
        dirlist.insert(0,'..')
        for i,item in enumerate(dirlist):
            if item == '': continue

            x = 0
            y = i*22

            def action(button):
                global dir
                item = button.text

                dir = dir.removesuffix('/')
                item = item.removesuffix('/')
                
                if item == '..':
                    if dir == '': return
                    ndir = f'/{dir.removesuffix('/').rsplit('/',1)[0]}'
                    if not ndir.endswith('/'):
                        ndir = f'{ndir}/'

                elif not dir:
                    ndir = f'/{item}/'

                elif '.' in item:
                    ndir = f'/{dir}/{item}'

                else:
                    ndir = f'/{dir}/{item}/'

                update_dir(app,ndir)

            b = ui.Button(
                position = (x,y),
                width = w.width,
                height = 20,
                text = item,
                size = 18,
                action = action,
                center = False,
                color = (70,70,70),
                hover_color = (75,75,75)
            ).add(w,1)

            w.buttons.append(b)



app = Application('filemanager','File Manager',1,open_app,ui.nothing,'assets/filemanager/filemanager_icon.png').launch()
