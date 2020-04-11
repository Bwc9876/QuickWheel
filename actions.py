import os
import shutil
import webbrowser
from zipfile import ZipFile


def open_app(arg):
    os.startfile(arg)


def open_file(arg):
    os.startfile(arg)


def open_file_with(args):
    os.system(rf'{args.split("~")[0]} {args.split("~")[1]}')


def run(args):
    command = ''
    first = True
    for i in args.split("~"):
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


def convert_dict_to_items(items_dict):
    out = ''
    for item in items_dict:
        if items_dict[item].get():
            out += item
            out += '~'
    return out[:-1]


def convert_items_to_dict(items, total_items):
    temp_dict = {}
    temp_list = items.split('~')
    for i in total_items:
        if not i.name == "0_0Base":
            if i.name in temp_list:
                temp_dict[i.name] = True
            else:
                temp_dict[i.name] = False
    return temp_dict
