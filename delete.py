import os
from tkinter import messagebox

import constants
import data


# noinspection PyUnusedLocal
def delete_event(ui, event):
    to_delete = ui.menuItems[0]
    ask_delete(ui, to_delete)


def remove_folder_from_folders(ui, to_delete):
    for folder in ui.totalFolders:
        if to_delete in data.decode_string_to_items(folder.folders, ui.totalFolders):
            new_list = data.decode_string_to_items(folder.folders, ui.totalFolders)
            new_list.remove(to_delete)
            folder.folders = data.encode_items_to_string(new_list)


def remove_item_from_folders(ui, to_delete):
    for folder in ui.totalFolders:
        if to_delete in data.decode_string_to_items(folder.items, ui.totalItems):
            new_items = data.decode_string_to_items(folder.items, ui.totalItems)
            new_items.remove(to_delete)
            folder.items = data.encode_items_to_string(new_items)


def ask_delete(ui, to_delete):
    actually_delete = messagebox.askyesno('Confirm', f'Are you sure you want to delete {to_delete.name}?')
    if actually_delete:
        delete(ui, to_delete)


def delete(ui, to_delete):
    if to_delete.name not in constants.non_editable:
        if to_delete.what_are_you() == "Item":
            os.remove(f"Data/Items/'{to_delete.name}'.json")
            ui.totalItems.remove(to_delete)
            remove_item_from_folders(ui, to_delete)
            ui.restart()
        else:
            os.remove(f"Data/Folders/'{ui.menuItems[0].name}'.json")
            ui.totalFolders.remove(ui.menuItems[0])
            remove_folder_from_folders(ui, to_delete)
            ui.restart()
