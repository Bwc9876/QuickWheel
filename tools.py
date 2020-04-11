import os
import shutil
import webbrowser
from zipfile import ZipFile


def open_app(app_path):
    os.startfile(app_path)


def open_file(file_path):
    os.startfile(file_path)


def open_file_with(file_path, app_path):
    os.system(rf'{app_path} {file_path}')


def run(*args):
    command = ''
    first = True
    for i in args:
        command += i
        if not first:
            command += ' '
        else:
            first = False
    os.system(command)


def web(url):
    webbrowser.open(url, new=2)


def steal_image(img_path):
    try:
        shutil.copy(img_path, 'Data/Images')
    except shutil.SameFileError:
        print("File already there")


def backup():
    try:
        os.remove("Backup.zip")
    except FileNotFoundError:
        print("No previous data")
    with ZipFile(f'Backup.zip', 'w') as zipObj:
        for folder_name, sub_folders, file_names in os.walk('Data'):
            for filename in file_names:
                file_path = os.path.join(folder_name, filename)
                zipObj.write(file_path)
        zipObj.close()


def restore():
    try:
        shutil.rmtree("Data")
    except FileNotFoundError:
        print("No previous data")
    with ZipFile(f'Backup.zip', 'r') as zipObj:
        zipObj.extractall()
