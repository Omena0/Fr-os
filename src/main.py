import engine as ui
from os import chdir
from classes import *

try: chdir('src')
except: ...

pygame = ui.pygame


def update_taskbar():
    global taskbar_icons, taskbar_area, taskbar_items
    taskbar_icons.children = []
    
    taskbar_area.changed = True
    taskbar_area.render()
    
    for i,app in enumerate(taskbar_items):
        ui.Button(
            position=(i*30,0),
            width=31,
            height=31,
            text = '',
            size = 0,
            action=app.launch,
            color=(35,35,35),
            hover_color=(35,35,35),
            corner_radius=5
        ).add(taskbar_icons)

        if app.icon:
            ui.Image(
                position=(i*30+3,0),
                width=25,
                height=25,
                image_path=app.icon
            ).add(taskbar_icons,2)
        else:
            ui.Text(
                position=(i*30+10,-5),
                text='-',
                size=50
            ).add(taskbar_icons,2)





apps:set[Application] = []

taskbar_items:list[Application] = []
start_pinned:list[Application] = []

init(globals(),locals())

### UI CODE ###


root = ui.Root(
    title="Fr Operating System V1.0.0 B1",
    bg=(0,0,0),
    res=size
)

root.show(True,extraFlag=pygame.NOFRAME)

## Title bar
bar = ui.Titlebar(
    root.title
).add(root,10)

## Wallpaper
wallpaper = ui.Image(
    (0,0),
    size[0],
    size[1],
    'assets/bg.png'
).add(root,-5)

## Taskbar
# Frame
taskbar = ui.Frame(
    (0,size[1]-30),
    size[1],
    30
).add(root,5)

# Area
taskbar_area = ui.Area(
    (0,0),
    size[0],
    30,
    (40,40,40),
    corner_radius=0
).add(taskbar)

# Items
taskbar_icons = ui.Frame(
    (5,0),
    size[0]-25,
    30
).add(taskbar,1)

START_ICON_WIDTH = 50
START_ICON_HEIGHT = 50

START_ICON_PADDING = 7

# Start menu app
def open_start(app_):
    y = size[1] - size[1]//3 - taskbar.height - 10
    w = ui.Window(
        (10,y),
        width = size[0]//3,
        height = size[1]//3,
        title = app_.name,
        on_quit=app_.quit
    ).add(root)
    app_.window = w
    
    i = -1
    for app in start_pinned:
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
        ui.Image(
            position=(x,y),
            width=START_ICON_WIDTH,
            height=START_ICON_HEIGHT,
            image_path=app.icon
        ).add(w,1)
        
        # Button
        ui.Button(
            position=(x-2,y-2),
            width=START_ICON_WIDTH+2,
            height=START_ICON_HEIGHT+2,
            text='',
            size = 0,
            action=app.launch,
            color=(60,60,60),
            hover_color=(60,60,60)
        ).add(w,1)

    w.changed = True


start_menu = Application('start','Applications',open_start,ui.nothing,'assets/fr_os.png').pin()



def event(event):
    global size
    if event.type in [pygame.VIDEORESIZE,pygame.WINDOWMAXIMIZED]:
        size = root.disp.get_size()
        wallpaper.width, wallpaper.height = size
        wallpaper.update_image()
        
        taskbar.setPos(0,size[1]-30)
        taskbar.width = size[1]

root.addListener(event)

while True:
    if not ui.update(): break
