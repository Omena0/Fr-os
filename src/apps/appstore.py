from classes import Application, size
import engine as ui
import socket
import json
import os

addr = ('127.0.0.1', 6969)

if 'settings' not in globals():
    settings = {'scale':1}

s = socket.socket()
s.settimeout(0.1)

try:
    s.connect(addr)
except WindowsError as e:
    raise ConnectionRefusedError('Could not connect to store server') from e


s.send(b'GET_APPS')

all_app_ids = s.recv(1024).decode().split(',')
categories = ['All']
store_all_apps = []
store_apps = {}

for app_id in all_app_ids:
    s.send(f'GET_APP|{app_id}'.encode())

    msg = s.recv(1024).decode().replace("'",'"')

    print(msg)

    app = json.loads(msg)

    if not app['category'] in categories:
        categories.append(app['category'])
    
    if not app['category'] in store_apps:
        store_apps[app['category']] = []

    store_apps[app['category']].append(app)
    store_all_apps.append(app)

selected_category = categories[0]

actions_categories = []
actions_tiles = []

def get_file(app,key,dir):
    global s
    if os.path.exists(dir): return True
    if app['files'][key] == '': return False
    print(f'Downloading: {key} to {dir}')
    s.send(f'GET_FILE|{app['files'][key]}'.encode())
    os.makedirs(dir.rsplit('/',1)[0],exist_ok=True)
    with open(dir,'wb') as f: f.write(s.recv(4294967296))
    return True

def open_app_page(store:Application,app):
    global w2, s, get_file, load_apps, ui

    x = size[0] // 2 - size[0]//3
    y = size[1] // 2 - size[1]//3
    
    # Create secondary window
    w2 = ui.Window(
        (x, y),
        width =  round(size[0]//3*settings['scale']),
        height = round(size[1]//2*settings['scale']),
        title = app['name']
    ).add(ui.root,100)
    store.windows.add(w2)

    # Download banner and icon
    icon_exists   = get_file(app,'icon',f'assets/{app['id']}/{app['id']}_icon.png')
    banner_exists = get_file(app,'banner',f'assets/{app['id']}/{app['id']}_banner.png')

    # Banner
    if banner_exists:
        ui.Image(
            (0,0),
            f'assets/{app['id']}/{app['id']}_banner.png',
            w2.width,
            w2.height//3
        ).add(w2)
    # No banner was found, display blank area with text
    else:
        ui.Area(
            (0,0),
            w2.width,
            w2.height//3,
            color=(70,70,70)
        ).add(w2)

        ui.Text(
            (w2.width//2-150,w2.height//6-15),
            'BANNER NOT FOUND',
            40,
            (85,85,85)
        ).add(w2,1)
    
    # Icon
    if icon_exists:
        ui.Image(
            (10,w2.height//6-w2.width//10),
            f'assets/{app['id']}/{app['id']}_icon.png',
            w2.width//5,
            w2.width//5
        ).add(w2,2)
    
    # App name text
    ui.Text(
        (20+w2.width//5,w2.height//6-30), app['name'], 40
    ).add(w2,4)

    # Install button
    ui.Button(
        (20+w2.width//5,30+w2.height//6-30),
        100,
        32,
        'Install',
        30,
        lambda: print('helloworld'),
        color = (70, 152, 240),
        hover_color = (75, 162, 250)
    ).add(w2,4)

    # Description text
    font_size = 100
    linecount = app['description'].count('\n')+1
    longest_line = len(max(app['description'].split('\n'),key=len))
    while True:
        if font_size//3 * longest_line < w2.width-15 and (font_size+3) * linecount < w2.height//3*2:
            break
        font_size -= 1
    
    ui.Text(
        (5,w2.height//3+10),
        app['description'],
        font_size,
    ).add(w2,4)




def install(app):
    global get_file, load_apps
    get_file(app,'app',f'apps/{app['id']}.py')
    load_apps()




def open_store_page(app:Application):
    global w, categories, actions_categories, update_apps, selected_category, store_apps, store_all_apps, store
    store = app

    x = size[0] // 2 - size[0]//3
    y = size[1] // 2 - size[1]//3
    w = ui.Window(
        (x, y),
        width = round(size[0]//2*settings['scale']),
        height = round(size[1]//2*settings['scale']),
        title = store.name,
        on_quit = store.quit
    ).add(ui.root)
    store.windows.add(w)

    # Categories
    category_list = ui.Frame(
        position=(10,10),
        width=100,
        height=round(w.height-20)
    ).add(w)

    category_background = ui.Area(
        position=(0,0),
        width=100,
        height=round(w.height-20),
        color=(60,60,60),
        corner_radius=10
    ).add(category_list)

    for category in categories:
        def press(category=category):
            global selected_category
            print(category)
            selected_category = category
            if selected_category.lower() == 'all':
                update_apps(store_all_apps)
            else:
                update_apps(store_apps[selected_category])
        actions_categories.append(press)

    for i,category in enumerate(categories):
        ui.Button(
            position=(category_background.width-95,i*40+10),
            width=90,
            height=30,
            text=category,
            size=25,
            action=actions_categories[i],
            color=(50,50,50),
            hover_color=(70,70,70)
        ).add(category_list,1)

    if selected_category.lower() == 'all':
        update_apps(store_all_apps)
    else:
        update_apps(store_apps[selected_category])

app_frame = None
def update_apps(apps:list):
    global w, actions_tiles, all_app_ids, app_frame
    if app_frame and app_frame in w.children: w.children.remove(app_frame)

    # App tiles
    app_frame = ui.Frame(
        position=(120,10),
        width=round(w.width-20),
        height=round(w.height-20)
    ).add(w)

    for app in apps:
        def press(app=app):
            global store, open_app_page
            open_app_page(store,app)
            print(app)
        actions_tiles.append(press)

    # Iterate over the apps and create a button for each one
    TILES_PER_ROW = round(w.width/150)
    print(TILES_PER_ROW)
    for i, app in enumerate(apps):
        ui.Button(
            position=(10 + (i % TILES_PER_ROW) * (round(w.width-150) // TILES_PER_ROW), 10 + (i // TILES_PER_ROW) * 110),
            width=round(w.width-170) // TILES_PER_ROW,
            height=100,
            text=app['name'],
            size=25,
            action=actions_tiles[i],
            color=(60,60,60),
            hover_color=(70,70,70)
        ).add(app_frame,1)



app = Application('appstore','Fr-store',open_store_page,ui.nothing,'assets/store.png').pin()



