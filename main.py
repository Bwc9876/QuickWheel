import os
from collections import deque
from tkinter import *

import interfaces
import item
import shapes
import tools
import window


class GUI:
    def __init__(self):
        self.Set = None
        self.canvas = None
        self.systemitems = []
        self.systemitems += [item.Item('~~Cancel', 'cancel.png', '~~exit~~')]
        self.systemitems += [item.Item('~~Add', 'plus.png', '~~Add~~')]
        self.systemitems += [item.Item('~~Back', 'back.png', '~~back~~')]
        self.folders = self.decode_folders()
        self.totalItems = self.decode_items()
        self.basefolder = self.folders[0]
        self.totalFolders = [self.basefolder] + self.folders
        self.currentFolder = self.basefolder
        self.folders = self.currentFolder.decode_string_to_folders(self.totalFolders)
        self.items = self.currentFolder.decode_string_to_items(self.totalItems)
        self.menuItems = self.folders + self.items + self.systemitems[:-1]
        self.root = Tk()
        self.init_render()
        self.init_window()

    def init_render(self):
        self.root, self.canvas = shapes.render_init(self.root, self.menuItems)

    def init_window(self):
        self.root = window.initialize_window(self.root, self.canvas)

    def regenerate_canvas(self):
        shapes.render_refresh(self.menuItems, self.canvas)

    # noinspection PyUnusedLocal
    def right(self, event):
        item_out = deque(self.menuItems)
        item_out.rotate(-1)
        self.menuItems = list(item_out)
        self.regenerate_canvas()

    # noinspection PyUnusedLocal
    def left(self, event):
        item_out = deque(self.menuItems)
        item_out.rotate(1)
        self.menuItems = list(item_out)
        self.regenerate_canvas()

    # TODO: Add animations for left and right arrow keys

    def encode_items(self):
        for itemin in self.items:
            if '~~' not in itemin.name:
                try:
                    os.remove(f"Items/{itemin.name}.json")
                except FileNotFoundError:
                    print("No previous data")
                f = open(f'Items/{itemin.name}.json', 'a+')
                instring = item.ItemEncoder().encode(itemin)
                print(instring)
                f.write(instring)
                f.close()

    def encode_folders(self):
        for iteme in self.totalFolders:
            if '~~' not in iteme.name:
                try:
                    os.remove(f"Folders/{iteme.name}.json")
                except FileNotFoundError:
                    print("No previous data")
                f = open(f'Folders/{iteme.name}.json', 'a+')
                instring = item.FolderEncoder().encode(iteme)
                print(instring)
                f.write(instring)
                f.close()

    @staticmethod
    def decode_items():
        out = []
        for file in os.listdir('Items'):
            f = open(f'Items/{file}', 'r')
            instring = f.read()
            out += [item.Item(None, None, None, instring)]
        return out

    @staticmethod
    def decode_folders():
        out = []
        for file in os.listdir('Folders'):
            f = open(f'Folders/{file}', 'r')
            instring = f.read()
            out += [item.Folder(None, None, None, None, None, data=instring)]
        return out

    # noinspection PyUnusedLocal
    def exit(self, event):
        self.root.destroy()

    def add_item(self, data):
        togo = item.Item(data[0].get(), data[1].get(), data[2].get())
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

        togo = item.Folder(data[0].get(), thing, data[1].get(), data[2].get(), data[3].get())
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
            if command == "~~exit~~":
                self.exit(None)
            elif command == "~~Add~~":
                self.root.withdraw()
                self.Set = Toplevel(self.root)
                self.Set.title("Add...")
                self.Set, ItemDat, FolderDat, Tab = interfaces.add_window(self.Set)
                b = Button(self.Set, text="Save", command=lambda data=[ItemDat, FolderDat, Tab]: self.add(data))
                b.pack()
                self.Set = window.center_add_window(self.Set)
                # TODO: UI revamp
            elif command == "~~back~~":
                self.back(None)
            # TODO: Add settings
            else:
                command_in = command.split("~")
                if command_in[0] == "launch":
                    tools.open_app(command_in[1])
                    self.root.destroy()
        elif what.what_are_you() == "Folder":
            self.switch_folder(what.name)

    # noinspection PyUnusedLocal
    def back(self, event):
        if not self.currentFolder.name == self.basefolder.name:
            self.switch_folder(self.currentFolder.parent)

    def refresh_menu(self):
        if not self.currentFolder.name == '0_0Base':
            self.menuItems = self.folders + self.items + [self.systemitems[0]] + [self.systemitems[-1]]
        else:
            self.menuItems = self.folders + self.items + self.systemitems[:-1]
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


UI = GUI()
UI = interfaces.init_input(UI)
UI.root.mainloop()
