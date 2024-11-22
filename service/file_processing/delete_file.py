import os


def delete_file_in_static(path: str):
    '''Удаление используемых файлов'''
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path): os.remove(file_path)