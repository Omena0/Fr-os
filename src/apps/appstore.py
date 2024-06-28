from classes import Application, size
import engine as ui
import socket
import json

addr = ('127.0.0.1', 6969)


s = socket.socket()

s.connect(addr)

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

def open_app(app:Application):
    global w, categories, actions_categories, update_apps, selected_category, store_apps, store_all_apps
    x = size[0] // 2 - size[0]//3
    y = size[1] // 2 - size[1]//3
    w = ui.Window(
        (x, y),
        width = round(size[0]//2*settings['scale']),
        height = round(size[1]//2*settings['scale']),
        title = app.name,
        on_quit = app.quit
    ).add(ui.root)
    app.window = w

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



app = Application('appstore','Fr-store',open_app,ui.nothing,'assets/store.png').pin()



