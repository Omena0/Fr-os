from classes import *
import engine as ui
import os

size = size[0]//2, size[1]//2

try: os.chdir('src')
except: ...

pygame = ui.pygame


# Settings
settings:dict[str,str|int|float|bool] = {
    "scale": 1,
    "use_dragging_rectangle": False
}

def update_taskbar():
    global taskbar_icons, taskbar_area, taskbar_items
    taskbar_icons.children = []
    
    taskbar_area.changed = True
    taskbar_area.render()
    
    taskbar.height = round(30*settings['scale'])
    
    taskbar_area.height = taskbar.height
    taskbar.setPos(0,round(root.disp.get_height()-30*settings['scale']))
    
    for i,app in enumerate(taskbar_items):
        ui.Button(
            position=(round(i*30*settings['scale']),0),
            width=round(31*settings['scale']),
            height=round(31*settings['scale']),
            text = '',
            size = 0,
            action=app.launch,
            color=(35,35,35),
            hover_color=(35,35,35),
            corner_radius=round(5*settings['scale'])
        ).add(taskbar_icons)

        if app.icon != '':
            ui.Image(
                position=(round((i*30+3)*settings['scale']),1+settings['scale']*2),
                width=25*settings['scale'],
                height=25*settings['scale'],
                image_path=app.icon,
                fs = fs
            ).add(taskbar_icons,2)
        else:
            ui.Text(
                position=(round((i*30+10)*settings['scale']),-5),
                text='-',
                size=50*settings['scale']
            ).add(taskbar_icons,2)

# Apps, taskbar and start menu
apps:set[Application] = set()
apps_dict:dict[str,Application] = {}
app_ids:set[str] = set()

taskbar_items:list[Application] = []

init(globals(),locals())

### UI CODE ###

root = ui.Root(
    title="Fr Operating System V1.0.1 B2",
    bg=(100,100,100),
    res=size
)

root.show(True)


## Title bar
bar = ui.Titlebar(
    root.title,
    border_radius=0
).add(root,10)

## Wallpaper
background = ui.Image(
    (0,0),
    'assets/bg.png',
    size[0],
    size[1],
    fs
).add(root,-5)

## Taskbar
# Frame
taskbar = ui.Frame(
    position=(0,round(size[1]-30*settings['scale'])),
    width=size[1],
    height=30
).add(root,5)

# Area
taskbar_area = ui.Area(
    position=(0,0),
    width=size[0],
    height=30,
    color=(40,40,40),
    corner_radius=0
).add(taskbar)

# Items
taskbar_icons = ui.Frame(
    position=(5,0),
    width=size[0]-25,
    height=30
).add(taskbar,1)

START_ICON_WIDTH = 50
START_ICON_HEIGHT = 50

START_ICON_PADDING = 7

# Apps menu
def open_apps_menu(app_):  # sourcery skip: remove-unnecessary-cast
    update_taskbar()
    y_ = size[1] - round(size[1]//3*settings['scale']) - taskbar.height - 10

    w = ui.Window(
        position = (10,y_+round(size[1]//3*settings['scale'])+taskbar.height+10),
        width = round(size[0]//4*settings['scale']),
        height = round(size[1]//3*settings['scale']),
        title = app_.name,
        on_quit=app_.quit
    ).add(root,999)
    app_.window = w
    
    i = -1
    for app in apps:
        if app == app_: continue
        i += 1

        x,y = 0,0
        #    START WIDTH    /   TOTAL WIDTH INCLUDING PADDING
        x = i * (START_ICON_WIDTH + START_ICON_PADDING) + 1 # +1 to prevent division by zero
        
        # WRAP ARROUND X
        while x > w.width:
            x -= w.width
            y += (START_ICON_HEIGHT + START_ICON_PADDING)
        
        # Add padding
        x += 5
        y += 5
        
        # Round to int
        x,y = int(x), int(y)
        
        
        # Icon
        if app.icon:
            ui.Image(
                position=(x,y),
                image_path=app.icon,
                width=START_ICON_WIDTH,
                height=START_ICON_HEIGHT,
                fs=fs
            ).add(w,3)
        
        # Button
        ui.Button(
            position=(x-2,y-2),
            width=START_ICON_WIDTH+2,
            height=START_ICON_HEIGHT+2,
            text='' if app.icon else '-',
            size = START_ICON_WIDTH*2,
            action=app.launch,
            color=(65,65,65),
            hover_color=(70,70,70)
        ).add(w,1)

    ui.Animation(
        component=w,
        length=40,
        endPos=(10,y_),
        easing = 'exp',
        ease_in = False
    ).start()
    

apps_menu = Application('applications','Applications',1,open_apps_menu,ui.nothing,'assets/core/fr_os.png').pin()


# Load apps

APPS_DIR = 'apps'

def unload(app_id):
    app_ids.remove(app_id)
    for app in apps:
        if app.id == app_id:
            apps.remove(app)
            try: taskbar_items.remove(app)
            except: ...
            app.quit()
            break
    update_taskbar()

def load_apps():
    with fs:
        for app in fs.listdir('/apps'):
            app_id = app.rsplit('.')[0]

            if app_id in app_ids:
                if app_id == 'appstore': continue
                unload(app_id)

            src = fs.read(f'{APPS_DIR}/{app}')
            globals().update(locals())
            try: exec(src,globals(),globals())
            except Exception as e:
                print(f'[AppManager] App "{app_id}" failed to load! [{e}]')
                raise e


load_apps()


def event(event):
    global size
    if event.type in [pygame.VIDEORESIZE,pygame.WINDOWMAXIMIZED]:
        size = root.disp.get_size()
        background.width, background.height = size
        background.update_image()
        
        taskbar_area.width = size[0]
        taskbar.setPos(0,size[1]-30)

root.addEventListener(event)

while ui.update():
    pass
