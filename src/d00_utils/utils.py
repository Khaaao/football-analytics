import os

def refresh_raw_input(file_name):
    if (os.path.isfile(f'data/raw/{file_name}')):
        os.remove(f'data/raw/{file_name}')
        print("File Deleted")
    with open(f'data/raw/{file_name}', 'w+'):
        print("File Created")