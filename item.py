import json
import os

import data
import folder


class Item:
    def __init__(self, name, img, command, args, data_in=None):
        if data_in is None:
            self.name = name
            self.image = img
            self.command = command
            self.args = args
        else:
            self.__dict__ = json.loads(data_in)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @staticmethod
    def what_are_you():
        return "Item"


def setup_system_items(ui):
    ui.systemitems += [Item('Cancel', 'cancel.png', '~~Exit~~', '')]
    ui.systemitems += [Item('Add', 'plus.png', '~~Add~~', '')]
    ui.systemitems += [Item('Appearance', 'appearance.png', '~~Set~~', '')]
    ui.systemitems += [Item('Reset Settings', 'reset.png', '~~Reset~~', '')]
    ui.systemitems += [Item('Backup Data', 'backup.png', '~~Backup~~', '')]
    ui.systemitems += [Item('Restore Data', 'restore.png', '~~Restore~~', '')]
    ui.systemitems += [Item('Edit Base Directory', 'edit_base.png', '~~Edit_Base~~', '')]
    ui.systemitems += [Item('Back', 'back.png', '~~Back~~', '')]


def decode_items():
    out = []
    if not os.path.exists('Data/Items'):
        os.mkdir('Data/Items')
    for file in os.listdir('Data/Items'):
        if file.split('.')[-1] == 'json':
            f = open(f"Data/Items/{file}", 'r')
            instring = f.read()
            out += [Item(None, None, None, None, data_in=instring)]
    return out


def initialize_user_items(ui):
    ui.totalItems = decode_items()
    ui.items = data.decode_string_to_items(ui.currentFolder.items, ui.totalItems)
    ui.items = data.decode_string_to_items(ui.currentFolder.items, ui.totalItems)


def item_image_handler(ui, data_in, remove_old=False):
    if data_in[1].image is None:
        if remove_old:
            image_name = ui.menuItems[0].image
        else:
            image_name = "None"
    else:
        image_name = data_in[1].image.split('/')[-1]
        data.steal_image(data_in[1].image)
    return image_name


def item_arg_handler(ui, data_in, remove_old=False):
    if data_in[1].arg1 is None:
        if data_in[2].get() == "web" or data_in[2] == "run":
            data_in[1].arg1 = data_in[4][4].get()
        else:
            if remove_old and ui.menuItems[0].command == "openwith":
                data_in[1].arg1 = ui.menuItems[0].args.split("~")[0]
            elif remove_old:
                data_in[1].arg1 = ui.menuItems[0].args
            else:
                ui.invalid_arg_warning()
    if data_in[1].arg2 is None:
        if data_in[2].get() == "openwith":
            if remove_old:
                data_in[1].arg2 = ui.menuItems[0].args.split("~")[1]
            else:
                ui.invalid_arg_warning()
    return data_in


def prepare_item_data(ui, data_in, remove_old=False):
    if not remove_old:
        if data_in[3].get() == "Base":
            data_in[3].set("0_0Base")
    image_name = item_image_handler(ui, data_in, remove_old=remove_old)
    data_in = item_arg_handler(ui, data_in, remove_old=remove_old)
    return data_in, image_name


def item_parent_handler(ui, data_in, togo):
    if data_in[3] == "noedit":
        for folder_in in ui.totalFolders:
            if ui.menuItems[0] in data.decode_string_to_items(folder_in.items, ui.totalItems):
                new_items = data.decode_string_to_items(folder_in.items, ui.totalItems)
                new_items.remove(ui.menuItems[0])
                folder_in.items = data.encode_items_to_string(new_items)
                folder_in.items = data.encode_items_to_string(
                    data.decode_string_to_items(folder_in.items, ui.totalItems) + [togo])
    else:
        folder_in = None
        for i in ui.totalFolders:
            if i.name == data_in[3].get():
                i.items = data.encode_items_to_string(data.decode_string_to_items(i.items, ui.totalItems) + [togo])
                folder_in = True
        if folder_in is None:
            ui.totalFolders[0].items = data.encode_items_to_string(
                data.decode_string_to_items(ui.totalFolders[0], ui.totalItems) + [togo])
    return data_in, togo


def item_edit_handler(ui, togo, remove_old=False):
    if remove_old:
        if not ui.menuItems[0].name == togo.name:
            ui.items += [togo]
        try:
            os.remove(f"Data/Items/'{ui.menuItems[0].name}'.json")
            ui.totalItems.remove(ui.menuItems[0])
            print(f"Old Data {ui.menuItems[0].name} removed")
        except FileNotFoundError:
            print("No previous data")


def add_item(ui, data_in, remove_old=False):
    data_in, image_name = prepare_item_data(ui, data_in, remove_old=remove_old)
    arg_dict = data.create_arg_dict(data_in)
    togo = Item(data_in[0].get(), image_name, data_in[2].get(), arg_dict[data_in[2].get()])
    data_in, togo = item_parent_handler(ui, data_in, togo)
    item_edit_handler(ui, togo, remove_old=remove_old)
    ui.totalItems += [togo]
    encode_items(ui)
    folder.encode_folders(ui)
    ui.Set.destroy()
    ui.restart()


def encode_items(ui):
    for itemin in ui.totalItems:
        if '~~' not in itemin.name:
            try:
                os.remove(f"Data/Items/'{itemin.name}'.json")
            except FileNotFoundError:
                print("No previous data")
            f = open(f"Data/Items/'{itemin.name}'.json", 'a+')
            instring = data.Encoder().encode(itemin)
            print(instring)
            f.write(instring)
            f.close()
