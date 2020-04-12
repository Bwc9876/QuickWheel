import os
import shutil
from json import JSONEncoder
from tkinter import messagebox
from zipfile import ZipFile


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


# noinspection PyUnusedLocal
def backup_event(ui, args):
    backup()
    messagebox.showinfo('Complete', 'All Data Has Been Backed Up')


def restore():
    try:
        shutil.rmtree("Data")
    except FileNotFoundError:
        print("No previous data")
    with ZipFile(f'Backup.zip', 'r') as zipObj:
        zipObj.extractall()


# noinspection PyUnusedLocal
def confirm_restore(ui, args):
    actually_restore = messagebox.askyesno('Are you sure?', 'This will override all data since this backup')
    if actually_restore:
        restore()
        messagebox.showinfo('Complete', 'All Data Has Been Restored')
        ui.restart()


def check_data(ui):
    check = [os.path.exists('Data'), os.path.exists('Data/Images'), os.path.exists('Data/Folders'),
             os.path.exists('Data/Settings.json')]
    if False in check:
        ui.ask_restore()
    if not os.path.exists("Backup.zip"):
        message = f"No backup data has been detected, would you like to back up now?"
        actually_backup = messagebox.askyesno('Backup?', message)
        if actually_backup:
            backup()
            messagebox.showinfo('Backup complete', "All data has been backed up, starting program")


def ask_restore(ui):
    if os.path.exists('Backup.zip'):
        message = f"Unable to start the program, would you like to restore data from a backup?"
        actually_restore = messagebox.askyesno('Unable to start', message)
        if actually_restore:
            restore()
            messagebox.showinfo('Complete', 'All Data Has Been Restored, please re-open the program')
            ui.exit(None)
        else:
            messagebox.showinfo('Unable to start', "Terminating program")
    else:
        messagebox.showinfo('Critical', "Unable to start the program, and no backup data is detected!")
        ui.exit(None)


def encode_items_to_string(item_list):
    out = ''
    for i in item_list:
        out += i.name
        out += '~'
    return out[:-1]


def decode_string_to_items(in_string, total):
    out = []
    for i in in_string.split('~'):
        for n in total:
            if i == n.name:
                out += [n]
    return out


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


def create_arg_dict(data):
    arg_dict = {
        "launch": data[1].arg1,
        "open": data[1].arg1,
        "openwith": f"{data[1].arg1}~{data[1].arg1}",
        "web": data[4][4].get(),
        "run": data[4][4].get()
    }
    return arg_dict


def steal_image(img_path):
    try:
        shutil.copy(img_path, 'Data/Images')
    except shutil.SameFileError:
        print("File already there")


class Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
