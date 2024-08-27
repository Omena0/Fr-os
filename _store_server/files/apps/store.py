from classes import Application, size
import engine as ui
import socket
import json

addr = ('127.0.0.1', 6969)

if 'settings' not in globals(): settings = {'scale': 1, 'use_dragging_rectangle': False}

s = socket.socket()
s.settimeout(0.1)

try:
    s.connect(addr)
except WindowsError as e:
    raise ConnectionRefusedError('Could not connect to store server') from e

def recvall(s:socket.socket):
    buf = bytes()
    while True:
        s.settimeout(0.1)

        try: a = s.recv(2048)
        except socket.timeout:
            break

        buf += a
    return buf

s.send(b'GET_APPS')

all_app_ids = recvall(s).decode().split(',')
categories = ['All']
store_all_apps = []
store_apps = {}

for app_id in all_app_ids:
    s.send(f'GET_APP|{app_id}'.encode())

    msg = s.recv(1024).decode().replace("'",'"')

    try: store_app = json.loads(msg)
    except json.JSONDecodeError:
        print(f'Could not parse JSON message: {msg}')
        continue

    if store_app['category'] not in categories:
        categories.append(store_app['category'])

    if store_app['category'] not in store_apps:
        store_apps[store_app['category']] = []

    store_apps[store_app['category']].append(store_app)
    store_all_apps.append(store_app)

selected_category = categories[0]

actions_categories = []
actions_tiles = []

install_buttons = {}

def get_file(app,key,dir):
    global s, fs_open
    #if fs.exists(dir): return True
    if app['files'][key] == '': return False

    print(f'Downloading: {key} to {dir}')
    s.send(f'GET_FILE|{app['files'][key]}'.encode())
    with fs_open(dir) as f:
        f.write(recvall(s))
    return True


def open_app_page(store:Application,app):
    global w2, s, get_file, load_apps, ui, fs, apps_dict, install_buttons

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
        try:
            ui.Image(
                (10,w2.height//6-w2.width//10),
                f'assets/{app['id']}/{app['id']}_icon.png',
                w2.width//5,
                w2.width//5,
                fs
            ).add(w2,2)

        except FileNotFoundError as e:
            print(f"File not found! [assets/{app['id']}/{app['id']}_icon.png]")

        except Exception as e:
            print(f'Error loading image, Corrupt? [{e}]')
            with fs:
                fs.delete(f'assets/{app['id']}/{app['id']}_icon.png')
            get_file(app,'icon',f'assets/{app['id']}/{app['id']}_icon.png')
            ui.Image(
                (10,w2.height//6-w2.width//10),
                f'assets/{app['id']}/{app['id']}_icon.png',
                w2.width//5,
                w2.width//5,
                fs
            ).add(w2,2)

    # App name text
    ui.Text(
        (20+w2.width//5,w2.height//6-30), app['name'], 40
    ).add(w2,4)

    # Install button

    width = 100
    print(apps_dict[app['id']].version)
    if app['version'] > apps_dict[app['id']].version:
        text = 'Update'
        action = lambda: update(app)
        color = (70, 152, 240)
        hover_color = (75, 162, 250)

    elif app['category'] == 'core':
        text = 'No Updates'
        action = ui.nothing
        color = (40, 40, 40)
        hover_color = (40, 40, 40)
        width = 125

    elif app['id'] in app_ids:
        text = 'Uninstall'
        action = lambda: uninstall(app)
        color = (255,60,60)
        hover_color = (255,70,70)
    else:
        text = 'Install'
        action = lambda: install(app)
        color = (70, 152, 240)
        hover_color = (75, 162, 250)

    a = ui.Button(
        (20+w2.width//5,30+w2.height//6-30),
        width,
        32,
        text,
        30,
        action,
        color = color,
        hover_color = hover_color
    ).add(w2,4)

    install_buttons[app['id']] = a
    print(install_buttons)

    # Description text
    font_size = 30
    linecount = app['description'].count('\n')+1
    longest_line = len(max(app['description'].split('\n'),key=len))
    while (
        font_size // 2.5 * longest_line >= w2.width - 15
        or (font_size + 3) * linecount >= w2.height // 3 * 2
    ):
        font_size -= 1

    ui.Text(
        (5,w2.height//3+10),
        app['description'],
        font_size,
    ).add(w2,4)

    return w2


def install(app):
    global get_file, load_apps, app_ids, install_buttons

    if app['id'] in app_ids: return

    store = app['id'] == 'store'

    print(f'Installing {app['name']}')
    get_file(app,'app',f'apps/{app['id']}.py')
    get_file(app,'icon',f'assets/{app['id']}/{app['id']}_icon.png')
    load_apps()

    if not store and app['id'] in app_ids:
        install_buttons[app['id']].text        = 'Uninstall'
        install_buttons[app['id']].action = lambda: uninstall(app)
        install_buttons[app['id']].color       = (255,60,60)
        install_buttons[app['id']].hover_color = (255,70,70)

    else:
        open_store_page(store_app)
        open_app_page(store_app,app)


def update(app):
    global unload
    unload(app['id'])
    install(app)

def uninstall(app):
    global unload

    if app['id'] not in app_ids: return
    
    print(f'Uninstalling {app["name"]}')
    unload(app['id'])
    with fs:
        fs.delete(f'apps/{app['id']}.py')
        for file in fs.listdir(f'assets/{app['id']}'):
            fs.delete(f'assets/{app["id"]}/{file}')
        load_apps()
    install_buttons[app['id']].text        = 'Install'
    install_buttons[app['id']].action = lambda: install(app)
    install_buttons[app['id']].color       = (70, 152, 240)
    install_buttons[app['id']].hover_color = (75, 162, 250)


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
    
    return w

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



store_app = Application('store','Fr-store',2,open_store_page,ui.nothing,'assets/store/store_icon.png').pin()



