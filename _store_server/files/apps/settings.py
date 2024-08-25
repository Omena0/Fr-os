import engine as ui
from classes import Application, size

if not 'settings' in globals(): settings = {'scale':1}

def set_scale(x):
    global open_app, START_ICON_HEIGHT, START_ICON_WIDTH, START_ICON_PADDING, update_taskbar, bar
    try:
        settings['scale'] = float(x)
    except Exception:
        settings['scale'] = 1

    # Taskbar
    update_taskbar()
    
    # Top bar
    bar.height = round(25*settings['scale'])
    bar.size = round(25*settings['scale'])
    bar.textPos = (5,bar.height//2-bar.size//3)
    bar.close.width = round(25*settings['scale'])
    bar.close.height = round(25*settings['scale'])
    bar.close.size = round(25*settings['scale'])
    bar.close.setPos(size[0]-bar.close.width,0)
    
    # Start Menu
    START_ICON_WIDTH = round(50*settings['scale'])
    START_ICON_HEIGHT = round(50*settings['scale'])

    START_ICON_PADDING = round(7*settings['scale'])


def open_app(app:Application):
    global set_scale
    x = size[0] // 2 - size[0]//3
    y = size[1] // 2 - size[1]//3
    w = ui.Window(
        (x, y),
        width = round(size[0]//3*settings['scale']),
        height = round(size[1]//3*settings['scale']),
        title = app.name,
        on_quit = app.quit
    ).add(ui.root)
    app.windows.add(w)
    
    # Scale
    ui.Text(
        position=(10,10),
        text='System Scale',
        size=round(25*settings['scale'])
    ).add(w)
    
        
    ui.Textbox(
        position=(round(w.width-round(100*settings['scale'])-10),10),
        width=round(100*settings['scale']),
        height=round(25*settings['scale']),
        size=round(30*settings['scale']),
        action=set_scale,
        text=str(settings['scale'])
    ).add(w)


app = Application('settings','Settings',open_app,ui.nothing,'assets/settings/settings_icon.png').pin(add_to_taskbar=False)



