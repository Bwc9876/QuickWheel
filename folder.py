import json
import os
from tkinter import Toplevel, Button

import data
import dialogue
import window


class Folder:
    def __init__(self, name, parent, icon, items, folders, data_in=None):
        if data_in is None:
            self.name = name
            self.parent = parent
            self.image = icon
            self.items = items
            self.folders = folders
        else:
            self.__dict__ = json.loads(data_in)

    @staticmethod
    def what_are_you():
        return "Folder"

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


def encode_folders(ui):
    for iteme in ui.totalFolders:
        if not iteme.name == "System":
            try:
                os.remove(f"Data/Folders/'{iteme.name}'.json")
            except FileNotFoundError:
                print("No previous data")
            f = open(f"Data/Folders/'{iteme.name}'.json", 'a+')
            instring = data.Encoder().encode(iteme)
            print(instring)
            f.write(instring)
            f.close()


def decode_folders():
    out = []
    for file in os.listdir('Data/Folders'):
        f = open(f'Data/Folders/{file}', 'r')
        instring = f.read()
        out += [Folder(None, None, None, None, None, data_in=instring)]
    return out


def edit_base_dir(ui, data_in):
    togo = Folder('0_0Base', "None", "None", data.convert_dict_to_items(data_in[0]),
                  data.convert_dict_to_items(data_in[1]))
    try:
        os.remove(f"Data/Folders/'0_0Base'.json")
        ui.totalFolders.pop(0)
        print(f"Old Data 0_0Base Removed")
    except FileNotFoundError:
        print("No previous data...?")
    ui.totalFolders.insert(0, togo)
    ui.basefolder = togo
    encode_folders(ui)
    ui.Set.destroy()
    ui.restart()


def prepare_folder_data(ui, data_in, remove_old=False):
    if data_in[4] == 'noedit':
        thing = ui.menuItems[0].parent
    else:
        if data_in[4].get() == "Base":
            data_in[4].set("0_0Base")
        thing = data_in[4].get()

    if data_in[1].image is None:
        if remove_old:
            image_name = ui.menuItems[0].image
        else:
            image_name = "None"
    else:
        image_name = data_in[1].image.split('/')[-1]
        data.steal_image(data_in[1].image)
    return data_in, thing, image_name


def folder_parent_handler(ui, data_in, togo):
    if data_in[4] == "noedit":
        if not data_in[0].get() == ui.menuItems[0].name:
            for folder in ui.totalFolders:
                if ui.menuItems[0] in data.decode_string_to_items(folder.folders, ui.totalFolders):
                    new_list = data.decode_string_to_items(folder.folders, ui.totalFolders)
                    new_list.remove(ui.menuItems[0])
                    folder.folders = data.encode_items_to_string(new_list)
                    folder.folders = data.encode_items_to_string(
                        data.decode_string_to_items(folder.folders, ui.totalFolders) + [togo])
    else:
        folder = None
        for i in ui.totalFolders:
            if i.name == data_in[4].get():
                i.folders = data.encode_items_to_string(
                    data.decode_string_to_items(i.folders, ui.totalFolders) + [togo])
                folder = True
        if folder is None:
            ui.totalFolders[0].folders = data.encode_items_to_string(
                data.decode_string_to_items(ui.totalFolders[0].folders, ui.totalFolders) + [togo])


def folder_edit_handler(ui, togo, remove_old=False):
    if remove_old:
        if not ui.menuItems[0].name == togo.name:
            ui.folders += [togo]
        try:
            os.remove(f"Data/Folders/'{ui.menuItems[0].name}'.json")
            ui.totalFolders.remove(ui.menuItems[0])
            print("Old Data removed")
        except FileNotFoundError:
            print("No previous data")


def add_folder(ui, data_in, remove_old=False):
    data_in, thing, image_name = prepare_folder_data(ui, data_in, remove_old=remove_old)
    togo = Folder(data_in[0].get(), thing, image_name, data.convert_dict_to_items(data_in[2]),
                  data.convert_dict_to_items(data_in[3]))
    ui.totalFolders += [togo]
    folder_parent_handler(ui, data_in, togo)
    folder_edit_handler(ui, togo, remove_old=remove_old)
    encode_folders(ui)
    ui.Set.destroy()
    ui.restart()


def initialize_system_folder(ui):
    ui.settings_folder = Folder("System", '0_0Base', 'cog.png', '', '')


def initialize_user_folders(ui):
    ui.totalFolders = decode_folders()
    ui.basefolder = ui.totalFolders[0]
    ui.currentFolder = ui.basefolder
    ui.folders = data.decode_string_to_items(ui.basefolder.folders, ui.totalFolders)


def switch_folder(ui, folder):
    target = None
    for i in ui.totalFolders:
        if i.name == folder:
            target = i
    if folder == "System":
        target = ui.settings_folder
    if target is not None:
        ui.items = data.decode_string_to_items(target.items, ui.totalItems)
        ui.folders = data.decode_string_to_items(target.folders, ui.totalFolders)
        ui.currentFolder = target
        ui.refresh_menu()


# noinspection PyUnusedLocal
def back(ui, event):
    if not ui.currentFolder.name == ui.basefolder.name:
        switch_folder(ui, ui.currentFolder.parent)


# noinspection PyUnusedLocal
def back_no_event(ui, args):
    back(ui, None)


# noinspection PyDefaultArgument,PyUnusedLocal
def edit_base(ui, args):
    ui.root.withdraw()
    ui.Set = Toplevel(ui.root)
    ui.Set.title("Edit Base")
    ui.Set, item_data, folder_data = dialogue.edit_base_window(ui.Set, ui.totalFolders[0],
                                                               ui.totalFolders, ui.totalItems)
    b = Button(ui.Set, text="Save",
               command=lambda data_in=[item_data, folder_data]: edit_base_dir(ui, data_in))
    b.pack()
    ui.Set = window.center_add_window(ui.Set)
