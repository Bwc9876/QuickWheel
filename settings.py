import json
import os
from tkinter import messagebox

import data


class Settings:
    def __init__(self, selector_pos, transparency, default_icon, default_folder_icon, wheel_color, inner_circle_color,
                 name_color, cursor_color, data_in=None):
        if data_in is None:
            self.selector_pos = selector_pos
            self.transparency = transparency
            self.default_icon = default_icon
            self.default_folder_icon = default_folder_icon
            self.wheel_color = wheel_color
            self.inner_circle_color = inner_circle_color
            self.name_color = name_color
            self.cursor_color = cursor_color
        else:
            self.__dict__ = json.loads(data_in)


def encode_settings(ui):
    instring = data.Encoder().encode(ui.settings)
    try:
        os.remove("Data/Settings.json")
    except FileNotFoundError:
        print("No previous data")
    f = open(f'Data/Settings.json', 'a+')
    print(instring)
    f.write(instring)
    f.close()


def initialize_settings(ui):
    ui.settings = decode_settings()


def decode_settings():
    f = open(f'Data/Settings.json', 'r')
    instring = f.read()
    out = Settings(None, None, None, None, None, None, None, None, data_in=instring)
    f.close()
    return out


def reset_settings(ui):
    instring = data.Encoder().encode(
        Settings('Top', 100, 'unknown.png', 'folder.png', "#d2d2d2", "black", "red", "grey"))
    try:
        os.remove("Data/Settings.json")
    except FileNotFoundError:
        print("No previous data")
    f = open(f'Data/Settings.json', 'a+')
    print(instring)
    f.write(instring)
    f.close()
    ui.settings = Settings('Top', 100, 'unknown.png', 'folder.png', "#d2d2d2", "black", "red", "grey")


# noinspection PyUnusedLocal
def ask_reset_settings(ui, args):
    actually_reset = messagebox.askyesno('Are you sure?', 'reset appearance settings?')
    if actually_reset:
        reset_settings(ui)


def prepare_settings_data(ui, data_in):
    if data_in[2].default_icon is None:
        data_in[2].default_icon = ui.settings.default_folder_icon
        icon_name = ui.settings.default_icon
    else:
        icon_name = data_in[2].default_icon.split('/')[-1]
        data.steal_image(data_in[2].default_icon)
    if data_in[2].default_folder is None:
        data_in[2].default_folder = ui.settings.default_folder_icon
        folder_name = data_in[2].default_folder
    else:
        folder_name = data_in[2].default_folder.split('/')[-1]
        data.steal_image(data_in[2].default_folder)
    if data_in[2].wheel_color is None:
        data_in[2].wheel_color = ui.settings.wheel_color
    if data_in[2].inner_color is None:
        data_in[2].inner_color = ui.settings.inner_circle_color
    if data_in[2].name_color is None:
        data_in[2].name_color = ui.settings.name_color
    if data_in[2].cursor_color is None:
        data_in[2].cursor_color = ui.settings.cursor_color
    return data_in, icon_name, folder_name


def save_settings(ui, data_in):
    data_in, icon_name, folder_name = prepare_settings_data(ui, data_in)
    togo = Settings(data_in[0].get(), data_in[1].get(), icon_name, folder_name, data_in[2].wheel_color,
                    data_in[2].inner_color, data_in[2].name_color, data_in[2].cursor_color)
    ui.settings = togo
    encode_settings(ui)
    ui.Set.destroy()
    ui.restart()
