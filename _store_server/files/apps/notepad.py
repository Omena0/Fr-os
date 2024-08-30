from classes import Application, size
import engine as ui

def open_app(app, *args, **kwargs):
    global fs_open, w

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

    if len(args) == 1:
        file = args[0]

        with fs_open(file) as file:
            text = file.read().decode(errors='ignore').replace('\x00','').replace('\r','')

    else:
        text = ''

    app.text = ui.Textbox(
        position = (0,0),
        width = w.width,
        height = w.height,
        size = 20,
        color = (70,70,70),
        focus_color = (70,70,70),
        hover_color = (70,70,70),
        text = text,
        corner_radius=0
    ).add(w,1)


app = Application('notepad','Notepad',1,open_app,ui.nothing,'')
app.add_meta({'extensions': ['txt','py','png']})
