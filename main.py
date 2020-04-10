import os
from collections import deque
from tkinter import *

import classes
import interfaces
import shapes
import tools
import window


class GUI:
    def __init__(self):
        self.settings = self.decode_settings()
        self.Set = None
        self.canvas = None
        self.systemitems = []
        self.systemitems += [classes.Item('Cancel', 'cancel.png', '~~Exit~~')]
        self.systemitems += [classes.Item('Add', 'plus.png', '~~Add~~')]
        self.systemitems += [classes.Item('Appearance', 'appearance.png', '~~Set~~')]
        self.systemitems += [classes.Item('Back', 'back.png', '~~Back~~')]
        self.folders = self.decode_folders()
        self.totalItems = self.decode_items()
        self.basefolder = self.folders[0]
        self.totalFolders = [self.basefolder] + self.folders
        self.totalFolders += [classes.Folder("System", '0_0Base', 'cog.png', 'Test', '')]
        self.currentFolder = self.basefolder
        self.folders = self.currentFolder.decode_string_to_folders(self.totalFolders)
        self.items = self.currentFolder.decode_string_to_items(self.totalItems)
        self.menuItems = self.folders + self.items + [self.systemitems[0]]
        self.root = Tk()
        self.init_render()
        self.init_window()

    def init_render(self):
        self.root, self.canvas = shapes.render_init(self.root, self.menuItems, self.settings)

    def init_window(self):
        self.root = window.initialize_window(self.root, self.canvas, self.settings)

    def regenerate_canvas(self):
        shapes.render_refresh(self.menuItems, self.canvas, self.settings)

    # noinspection PyUnusedLocal
    def direction_handler(self, event, input_direction):
        positions = {
            'Top': [self.left, self.right],
            'Bottom': [self.right, self.left],
        }
        positions[self.settings.selector_pos][input_direction]()

    def right(self):
        item_out = deque(self.menuItems)
        item_out.rotate(-1)
        self.menuItems = list(item_out)
        self.regenerate_canvas()

    def left(self):
        item_out = deque(self.menuItems)
        item_out.rotate(1)
        self.menuItems = list(item_out)
        self.regenerate_canvas()

    def encode_items(self):
        for itemin in self.items:
            if '~~' not in itemin.name:
                try:
                    os.remove(f"Data/Items/{itemin.name}.json")
                except FileNotFoundError:
                    print("No previous data")
                f = open(f'Data/Items/{itemin.name}.json', 'a+')
                instring = classes.ItemEncoder().encode(itemin)
                print(instring)
                f.write(instring)
                f.close()

    def encode_folders(self):
        for iteme in self.totalFolders:
            if '~~' not in iteme.name:
                try:
                    os.remove(f"Data/Folders/{iteme.name}.json")
                except FileNotFoundError:
                    print("No previous data")
                f = open(f'Data/Folders/{iteme.name}.json', 'a+')
                instring = classes.FolderEncoder().encode(iteme)
                print(instring)
                f.write(instring)
                f.close()

    @staticmethod
    def decode_items():
        out = []
        for file in os.listdir('Data/Items'):
            if file.split('.')[-1] == 'json':
                f = open(f'Data/Items/{file}', 'r')
                instring = f.read()
                out += [classes.Item(None, None, None, instring)]
        return out

    @staticmethod
    def decode_folders():
        out = []
        for file in os.listdir('Data/Folders'):
            f = open(f'Data/Folders/{file}', 'r')
            instring = f.read()
            out += [classes.Folder(None, None, None, None, None, data=instring)]
        return out

    # noinspection PyUnusedLocal
    def exit(self, event):
        self.root.destroy()

    def add_item(self, data):
        if data[1].image is None:
            image_name = "None"
        else:
            image_name = data[1].image.split('/')[-1]
            tools.steal_image(data[1].image)

        togo = classes.Item(data[0].get(), image_name, data[2].get())
        folder = None
        for i in self.totalFolders:
            if i.name == data[3].get():
                i.items = i.encode_items_to_string(i.decode_string_to_items(self.totalItems) + [togo])
                folder = True
        if folder is None:
            self.totalFolders[0].items = self.totalFolders[0].encode_items_to_string(
                self.totalFolders[0].decode_string_to_items(self.totalItems) + [togo])
        self.items += [togo]
        self.encode_items()
        self.encode_folders()
        self.root.destroy()
        self.Set.destroy()

    def add_folder(self, data):
        if data[4].get() == '':
            thing = "0_0Base"
        else:
            thing = data[4].get()

        if data[1].image is None:
            image_name = "None"
        else:
            image_name = data[1].image.split('/')[-1]
            tools.steal_image(data[1].image)

        togo = classes.Folder(data[0].get(), thing, image_name, data[2].get(), data[3].get())
        folder = None

        for i in self.totalFolders:
            if i.name == data[4].get():
                i.folders = i.encode_folders_to_string(i.decode_string_to_folders(self.totalFolders) + [togo])
                folder = True
        if folder is None:
            self.totalFolders[0].folders = self.totalFolders[0].encode_folders_to_string(
                self.totalFolders[0].decode_string_to_folders(self.totalFolders) + [togo])

        self.totalFolders += [togo]
        self.encode_folders()
        self.root.destroy()
        self.Set.destroy()

    def save_settings(self, data):
        if data[2].default_icon is None:
            data[2].default_icon = self.settings.default_folder_icon
            icon_name = self.settings.default_icon
        else:
            icon_name = data[2].default_icon.split('/')[-1]
            tools.steal_image(data[2].default_icon)
        if data[2].default_folder is None:
            data[2].default_folder = self.settings.default_folder_icon
            folder_name = data[2].default_folder
        else:
            folder_name = data[2].default_folder.split('/')[-1]
            tools.steal_image(data[2].default_folder)
        if data[2].wheel_color is None:
            data[2].wheel_color = self.settings.wheel_color
        if data[2].inner_color is None:
            data[2].inner_color = self.settings.inner_circle_color
        if data[2].name_color is None:
            data[2].name_color = self.settings.name_color
        if data[2].cursor_color is None:
            data[2].cursor_color = self.settings.cursor_color

        togo = classes.Settings(data[0].get(), data[1].get(), icon_name, folder_name, data[2].wheel_color,
                                data[2].inner_color, data[2].name_color, data[2].cursor_color)
        self.settings = togo
        self.encode_settings()
        self.root.destroy()
        self.Set.destroy()

    def add(self, data):
        what = data[2].tab(data[2].select(), 'text')
        if what == "Item":
            self.add_item(data[0])
        else:
            self.add_folder(data[1])

    # noinspection PyDefaultArgument,PyUnusedLocal
    def invoke(self, event):
        what = self.menuItems[0]
        if what.what_are_you() == "Item":
            command = what.command
            if command == "~~Exit~~":
                self.exit(None)
            elif command == "~~Add~~":
                self.root.withdraw()
                self.Set = Toplevel(self.root)
                self.Set.title("Add...")
                self.Set, ItemDat, FolderDat, Tab = interfaces.add_window(self.Set)
                b = Button(self.Set, text="Save", command=lambda data_in=[ItemDat, FolderDat, Tab]: self.add(data_in))
                b.pack()
                self.Set = window.center_add_window(self.Set)
            elif command == "~~Back~~":
                self.back(None)
            elif command == "~~Set~~":
                self.root.withdraw()
                self.Set = Toplevel(self.root)
                self.Set.title("Settings")
                self.Set, data = interfaces.edit_settings(self.Set, self.settings)
                b = Button(self.Set, text="Save", command=lambda data_in=data: self.save_settings(data_in))
                b.pack()
                self.Set = window.center_add_window(self.Set)
            elif command == "~~Dummy~~":
                print(f"Dummy command triggered")
            else:
                command_in = command.split("~")
                if command_in[0] == "launch":
                    tools.open_app(command_in[1])
                    self.root.destroy()
                elif command_in[0] == "open":
                    tools.open_file(command_in[1])
                    self.root.destroy()
                elif command_in[0] == "openwith":
                    tools.open_file_with(command_in[1], command_in[2])
                    self.root.destroy()
                elif command_in[0] == "run":
                    tools.run(command_in[0:])
                    self.root.destroy()
                elif command_in[0] == "web":
                    tools.web(command_in[1])
                    self.root.destroy()

        elif what.what_are_you() == "Folder":
            self.switch_folder(what.name)

    # noinspection PyUnusedLocal
    def back(self, event):
        if not self.currentFolder.name == self.basefolder.name:
            self.switch_folder(self.currentFolder.parent)

    def refresh_menu(self):
        if self.currentFolder.name == '0_0Base':
            self.menuItems = self.folders + self.items + [self.systemitems[0]]
        elif self.currentFolder.name == "System":
            self.menuItems = self.folders + self.items + self.systemitems[1:]
        else:
            self.menuItems = self.folders + self.items + [self.systemitems[0]] + [self.systemitems[-1]]
        self.regenerate_canvas()

    def switch_folder(self, folder):
        target = None
        for i in self.totalFolders:
            if i.name == folder:
                target = i
        if target is not None:
            self.items = target.decode_string_to_items(self.totalItems)
            self.folders = target.decode_string_to_folders(self.totalFolders)
            self.currentFolder = target
            self.refresh_menu()

    def encode_settings(self):
        instring = classes.SettingsEncoder().encode(self.settings)
        try:
            os.remove("Data/Settings.json")
        except FileNotFoundError:
            print("No previous data")
        f = open(f'Data/Settings.json', 'a+')
        print(instring)
        f.write(instring)
        f.close()

    @staticmethod
    def decode_settings():
        f = open(f'Data/Settings.json', 'r')
        instring = f.read()
        out = classes.Settings(None, None, None, None, None, None, None, None, data=instring)
        return out

    def reset_settings(self):
        instring = classes.SettingsEncoder().encode(
            classes.Settings('Top', 100, 'unknown.png', 'folder.png', "#d2d2d2", "black", "red", "grey"))
        try:
            os.remove("Data/Settings.json")
        except FileNotFoundError:
            print("No previous data")
        f = open(f'Data/Settings.json', 'a+')
        print(instring)
        f.write(instring)
        f.close()
        self.root.destroy()


def main():
    ui = GUI()
    ui = interfaces.init_input(ui)
    ui.root.mainloop()


main()
