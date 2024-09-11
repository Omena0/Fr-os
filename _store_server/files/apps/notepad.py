from classes import Application, size
import engine as ui

def open_app(app, *args, **kwargs):
    global fs_open, w, file

    if len(args) == 1:
        file = args[0]

        with fs_open(file) as f:
            text = f.read().decode(errors='ignore').replace('\x00','').replace('\r','')

    else:
        text = ''

    x = size[0] // 2 - size[0]//3
    y = size[1] // 2 - size[1]//3
    w = ui.Window(
        position = (x,y),
        width=400,
        height=300,
        title=f'{app.name} - {file}'
    ).add(ui.root)
    app.window = w
    app.windows.add(w)

    def save(text):
        global app, file
        with fs_open(file) as f:
            f.write(text)

    app.text = ui.Textbox(
        position = (0,0),
        width = w.width,
        height = w.height,
        size = 20,
        color = (70,70,70),
        focus_color = (70,70,70),
        hover_color = (70,70,70),
        text = text,
        corner_radius=0,
        action = save
    ).add(w,1)


app = Application('notepad','Notepad',1,open_app,ui.nothing,'')
app.add_meta({'extensions': ['txt','py']})
