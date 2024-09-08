from classes import Application, size
import engine as ui

def open_app(app:Application):
    global fs,w

    x = size[0] // 2 - size[0]//3
    y = size[1] // 2 - size[1]//3
    w = ui.Window(
        position = (x,y),
        width=400,
        height=300,
        title=app.name
    ).add(ui.root)
    app.window = w
    app.windows.add(w)

    update_dir(app,'/')

def update_dir(app,d:str):
    global w, dir

    dir = d

    for i in w.children:
        try:
            w.remove(i)
        except: ...

    with fs:
        dirlist = fs.listdir(dir)
        dirlist.insert(0,'..')
        for i,item in enumerate(dirlist):
            if item == '': continue

            x = 0
            y = i*22

            def action(button=None):
                global dir, apps
                item = button.text

                if item == '..':
                    if dir == '': return
                    ndir = f'/{dir.removesuffix('/').rsplit('/',1)[0]}'
                    ndir = f'/{ndir.replace('//','')}/'

                else:
                    if dir == '/':
                        ndir = f'/{item}'
                    else:
                        ndir = f'/{dir.strip('/')}/{item}'

                if not ndir.endswith('/'):
                    if not fs.exists(ndir): ...
                    for app_ in apps:
                        if ndir.rsplit('.')[1] in app_.meta.get('extensions',[]):
                            print(f'Launching {app_.name}')
                            app_.launch(ndir)
                            return

                else:
                    print(ndir)
                    update_dir(app,ndir)

            ui.Button(
                position = (x,y),
                width = w.width,
                height = 20,
                text = item,
                size = 18,
                action = action,
                center = False,
                color = (70,70,70),
                hover_color = (75,75,75),
                corner_radius=2
            ).add(w,1)



app = Application('filemanager','File Manager',1,open_app,ui.nothing,'assets/filemanager/filemanager_icon.png')

