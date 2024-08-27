from classes import *
from sys import argv

with fs:
    if argv[1] == 'write':
        argv.append(argv[2])
        with open(argv[2], 'rb') as file:
            data = file.read()
            fs.write(f'/{argv[3]}', data)

    elif argv[1] == 'read':
        print(fs.read(f'/{argv[2]}'))
    
    elif argv[1] == 'delete':
        if argv[2].endswith('/*'):
            argv[2] = argv[2].removesuffix('/*')
            for file in fs.listdir(argv[2]):
                fs.delete(file)
        else:
            fs.delete(f'{argv[2]}')

    elif argv[1] == 'list':
        for i in fs.files.keys():
            print(i)


