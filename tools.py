import os
import shutil
import webbrowser


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
