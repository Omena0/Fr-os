from threading import Thread
import socket
import json

FILES_PATH = 'files'

apps = json.load(open('apps.json'))
apps_list = [id for id in apps]

print(apps)

files = {}
for id,app in apps.items():
    files[hash(f'{id}.py')] = f'{FILES_PATH}/{id}.py'
    files[hash(f'{id}_icon.png')] = f'{FILES_PATH}/{id}_icon.png'
    files[hash(f'{id}_banner.png')] = f'{FILES_PATH}/{id}_banner.png'


addr = ('127.0.0.1', 6969)


s = socket.socket()

s.bind(addr)

s.listen(5)

def csHandler(cs:socket.socket,addr):
    while True:
        try:
            msg = cs.recv(1024).decode().split('|')

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
