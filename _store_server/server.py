from threading import Thread
import hashlib
import socket
import json
import os

try: os.chdir('_store_server')
except: ...

FILES_PATH = 'files'

def load_apps():
    global apps, apps_list, files
    with open('apps.json') as f:
        apps = json.load(f)

    apps_list = [id for id in apps]

    files = {}
    for id,app in apps.items():
        files[hashlib.sha1(f'{id}.py'.encode()).hexdigest()] = f'{FILES_PATH}/apps/{id}.py'
        files[hashlib.sha1(f'{id}_icon.png'.encode()).hexdigest()] = f'{FILES_PATH}/icons/{id}_icon.png'
        files[hashlib.sha1(f'{id}_banner.png'.encode()).hexdigest()] = f'{FILES_PATH}/banners/{id}_banner.png'

load_apps()

print('---- Files ----')
for hash,name in files.items():
    print(f'{name:<40} - {hash:40}')


addr = ('127.0.0.1', 6969)


s = socket.socket()

s.bind(addr)

s.listen(5)

def csHandler(cs:socket.socket,addr):
    while True:
        try:
            msg = cs.recv(1024).decode()
            if msg == '':
                cs.send(b' ')
                continue

            msg = msg.strip().split('|')

            if msg[0] == 'GET_APPS':
                load_apps()
                a = f'{','.join(apps_list)}'
                print(a)
                cs.send(a.encode())

            elif msg[0] == 'GET_APP':
                load_apps()
                if msg[1] not in apps_list:
                    cs.send(b'INVALID')
                    print('INVALID')
                    continue

                a = f'{apps[msg[1]]}'
                print(a)
                cs.send(a.encode())

            elif msg[0] == 'GET_FILE':
                load_apps()
                if msg[1] not in files:
                    cs.send(b'INVALID')
                    print('INVALID')
                    continue

                with open(files[msg[1]],'rb') as file:
                    cs.sendfile(file)
                    del file

        except Exception as e:
            print(e)
            try:
                cs.close()
            except: ...
            print(f'[-] {addr}')
            del cs
            break


while True:
    cs,addr = s.accept()
    Thread(target=csHandler, args=(cs,addr), daemon=True).start()
    print(f'[+] {addr}')
