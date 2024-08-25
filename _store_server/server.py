from threading import Thread
import hashlib
import socket
import json
import os

try: os.chdir('_store_server')
except: ...

FILES_PATH = 'files'

apps = json.load(open('apps.json'))
apps_list = [id for id in apps]

files = {}
for id,app in apps.items():
    files[hashlib.sha1(f'{id}.py'.encode()).hexdigest()] = f'{FILES_PATH}/apps/{id}.py'
    files[hashlib.sha1(f'{id}_icon.png'.encode()).hexdigest()] = f'{FILES_PATH}/icons/{id}_icon.png'
    files[hashlib.sha1(f'{id}_banner.png'.encode()).hexdigest()] = f'{FILES_PATH}/banners/{id}_banner.png'


for file in files.items():
    print(file)


addr = ('127.0.0.1', 6969)


s = socket.socket()

s.bind(addr)

s.listen(5)

def csHandler(cs:socket.socket,addr):
    while True:
        try:
            msg = cs.recv(1024).decode()
            if msg == '': continue
            msg = msg.strip().split('|')
            print(msg)

            if msg[0] == 'GET_APPS':
                a = f'{','.join(apps_list)}'
                print(a)
                cs.send(a.encode())

            elif msg[0] == 'GET_APP':
                if msg[1] not in apps_list:
                    cs.send(b'INVALID')
                    print('INVALID')
                    continue
                
                a = f'{apps[msg[1]]}'
                print(a)
                cs.send(a.encode())

            elif msg[0] == 'GET_FILE':
                if not msg[1] in files:
                    cs.send(b'INVALID')
                    print('INVALID')
                    continue

                with open(files[msg[1]],'rb') as file:
                    cs.sendfile(file)

        except Exception as e:
            print(e)
            try:
                cs.close()
            except: ...
            print(f'[-] {addr}')
            break


while True:
    cs,addr = s.accept()
    Thread(target=csHandler, args=(cs,addr)).start()
    print(f'[+] {addr}')
