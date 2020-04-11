import os
from collections import deque
from tkinter import *
from tkinter import messagebox

import classes
import interfaces
import shapes
import tools
import window


# noinspection PyUnusedLocal
class GUI:
    def __init__(self):
        self.root = Tk()
        self.check_data()
        self.non_editable = [
            "Exit",
            "Add",
            "Set",
            "Back",
            "Appearance",
            "System",
            "Cancel",
            "Edit Base Directory",
            "Restore Data",
            "Backup Data",
            "Reset Settings"
        ]
        self.settings = self.decode_settings()
        self.Set = None
        self.canvas = None
        self.systemitems = []
        self.systemitems += [classes.Item('Cancel', 'cancel.png', '~~Exit~~')]
        self.systemitems += [classes.Item('Add', 'plus.png', '~~Add~~')]
        self.systemitems += [classes.Item('Appearance', 'appearance.png', '~~Set~~')]
        self.systemitems += [classes.Item('Reset Settings', 'reset.png', '~~Reset~~')]
        self.systemitems += [classes.Item('Backup Data', 'backup.png', '~~Backup~~')]
        self.systemitems += [classes.Item('Restore Data', 'restore.png', '~~Restore~~')]
        self.systemitems += [classes.Item('Edit Base Directory', 'edit_base.png', '~~Edit_Base~~')]
        self.systemitems += [classes.Item('Back', 'back.png', '~~Back~~')]
        self.folders = self.decode_folders()
        self.totalItems = self.decode_items()
        self.basefolder = self.folders[0]
        self.totalFolders = self.folders
        self.settings_folder = classes.Folder("System", '0_0Base', 'cog.png', 'Test', '')
        self.currentFolder = self.basefolder
        self.folders = self.currentFolder.decode_string_to_folders(self.totalFolders)
        self.items = self.currentFolder.decode_string_to_items(self.totalItems)
        self.menuItems = self.folders + self.items + [self.systemitems[0]] + [self.settings_folder]
        self.init_render()
        self.init_window()

    def init_render(self):
        self.root, self.canvas = shapes.render_init(self.root, self.menuItems, self.settings)

    def init_window(self):
        self.root = window.initialize_window(self.root, self.canvas, self.settings)

    def regenerate_canvas(self):
        self.root = window.update_window(self.root, self.settings)
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
        for itemin in self.totalItems:
            if '~~' not in itemin.name:
                try:
                    os.remove(f"Data/Items/'{itemin.name}'.json")
                except FileNotFoundError:
                    print("No previous data")
                f = open(f"Data/Items/'{itemin.name}'.json", 'a+')
                instring = classes.ItemEncoder().encode(itemin)
                print(instring)
                f.write(instring)
                f.close()

    # noinspection PyDefaultArgument
    def edit_selected(self, event):
        if self.menuItems[0].name not in self.non_editable:
            old_item = self.menuItems[0]
            self.root.withdraw()
            self.Set = Toplevel(self.root)
            self.Set.title(f"Edit {old_item.name}")
            self.Set, dat = interfaces.edit_window(self.Set, old_item, self.totalFolders, self.totalItems)
            if old_item.what_are_you() == "Item":
                b = Button(self.Set, text=f"Save {old_item.name}",
                           command=lambda data_in=dat: self.add_item(data_in, remove_old=True))
                b.pack()
            elif old_item.what_are_you() == "Folder":
                b = Button(self.Set, text=f"Save {old_item.name}",
                           command=lambda data_in=dat: self.add_folder(data_in, remove_old=True))
                b.pack()
            self.Set = window.center_add_window(self.Set)

    def encode_folders(self):
        for iteme in self.totalFolders:
            if not iteme.name == "System":
                try:
                    os.remove(f"Data/Folders/'{iteme.name}'.json")
                except FileNotFoundError:
                    print("No previous data")
                f = open(f"Data/Folders/'{iteme.name}'.json", 'a+')
                instring = classes.FolderEncoder().encode(iteme)
                print(instring)
                f.write(instring)
                f.close()

    @staticmethod
    def decode_items():
        out = []
        if not os.path.exists('Data/Items'):
            os.mkdir('Data/Items')
        for file in os.listdir('Data/Items'):
            if file.split('.')[-1] == 'json':
                f = open(f"Data/Items/{file}", 'r')
                instring = f.read()
                out += [classes.Item(None, None, None, instring)]
        return out

    def delete(self, event):
        to_delete = self.menuItems[0]
        if to_delete.name not in self.non_editable:
            actually_delete = messagebox.askyesno('Confirm', f'Are you sure you want to delete {to_delete.name}?')
            if actually_delete:
                if to_delete.what_are_you() == "Item":
                    os.remove(f"Data/Items/'{to_delete.name}'.json")
                    self.totalItems.remove(to_delete)
                    for folder in self.totalFolders:
                        if to_delete in folder.decode_string_to_items(self.totalItems):
                            new_items = folder.decode_string_to_items(self.totalItems)
                            new_items.remove(to_delete)
                            folder.items = folder.encode_items_to_string(new_items)
                    self.restart()
                else:
                    os.remove(f"Data/Folders/'{self.menuItems[0].name}'.json")
                    self.totalFolders.remove(self.menuItems[0])
                    for folder in self.totalFolders:
                        if to_delete in folder.decode_string_to_folders(self.totalFolders):
                            new_list = folder.decode_string_to_folders(self.totalFolders)
                            new_list.remove(to_delete)
                            folder.folders = folder.encode_folders_to_string(new_list)
                    self.restart()

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

    def edit_base_dir(self, data):
        togo = classes.Folder('0_0Base', "None", "None", tools.convert_dict_to_items(data[0]),
                              tools.convert_dict_to_items(data[1]))
        try:
            os.remove(f"Data/Folders/'0_0Base'.json")
            self.totalFolders.pop(0)
            print(f"Old Data 0_0Base Removed")
        except FileNotFoundError:
            print("No previous data...?")
        self.totalFolders.insert(0, togo)
        self.basefolder = togo
        self.encode_folders()
        self.Set.destroy()
        self.restart()

    def add_item(self, data, remove_old=False):
        if not remove_old:
            if data[3].get() == "Base":
                data[3].set("0_0Base")
        if data[1].image is None:
            if remove_old:
                image_name = self.menuItems[0].image
            else:
                image_name = "None"
        else:
            image_name = data[1].image.split('/')[-1]
            tools.steal_image(data[1].image)

        togo = classes.Item(data[0].get(), image_name, data[2].get())
        if data[3] == "noedit":
            print("EDIT TRIGGERED")
            for folder in self.totalFolders:
                if self.menuItems[0] in folder.decode_string_to_items(self.totalItems):
                    new_items = folder.decode_string_to_items(self.totalItems)
                    new_items.remove(self.menuItems[0])
                    folder.items = folder.encode_items_to_string(new_items)
                    folder.items = folder.encode_items_to_string(
                        folder.decode_string_to_items(self.totalItems) + [togo])
        else:
            folder = None
            for i in self.totalFolders:
                if i.name == data[3].get():
                    i.items = i.encode_items_to_string(i.decode_string_to_items(self.totalItems) + [togo])
                    folder = True
            if folder is None:
                self.totalFolders[0].items = self.totalFolders[0].encode_items_to_string(
                    self.totalFolders[0].decode_string_to_items(self.totalItems) + [togo])

        if remove_old:
            try:
                os.remove(f"Data/Items/'{self.menuItems[0].name}'.json")
                self.totalItems.remove(self.menuItems[0])
                print(f"Old Data {self.menuItems[0].name} removed")
            except FileNotFoundError:
                print("No previous data")

        self.totalItems += [togo]
        if remove_old:
            self.items += [togo]
        self.encode_items()
        self.encode_folders()
        self.Set.destroy()
        self.restart()

    def check_data(self):
        check = [os.path.exists('Data'), os.path.exists('Data/Images'), os.path.exists('Data/Folders'),
                 os.path.exists('Data/Settings.json')]
        if False in check:
            self.ask_restore()
        if not os.path.exists("Backup.zip"):
            message = f"No backup data has been detected, would you like to back up now?"
            actually_backup = messagebox.askyesno('Backup?', message)
            messagebox.showinfo('Backup complete', "All data has been backed up, starting program")
            if actually_backup:
                tools.backup()

    def ask_restore(self):
        if os.path.exists('Backup.zip'):
            message = f"Unable to start the program, would you like to restore data from a backup?"
            actually_restore = messagebox.askyesno('Unable to start', message)
            if actually_restore:
                tools.restore()
                messagebox.showinfo('Complete', 'All Data Has Been Restored, please re-open the program')
                self.exit(None)
            else:
                messagebox.showinfo('Unable to start', "Terminating program")
        else:
            messagebox.showinfo('Critical', "Unable to start the program, and no backup data is detected!")
            self.exit(None)

    def add_folder(self, data, remove_old=False):

        if data[4] == 'noedit':
            thing = self.menuItems[0].parent
        else:
            if data[4].get() == "Base":
                data[4].set("0_0Base")
            thing = data[4].get()

        if data[1].image is None:
            if remove_old:
                image_name = self.menuItems[0].image
            else:
                image_name = "None"
        else:
            image_name = data[1].image.split('/')[-1]
            tools.steal_image(data[1].image)
        print(tools.convert_dict_to_items(data[3]))
        togo = classes.Folder(data[0].get(), thing, image_name, tools.convert_dict_to_items(data[2]),
                              tools.convert_dict_to_items(data[3]))
        self.totalFolders += [togo]
        if remove_old:
            self.folders += [togo]
        if data[4] == "noedit":
            if not data[0].get() == self.menuItems[0].name:
                for folder in self.totalFolders:
                    if self.menuItems[0] in folder.decode_string_to_folders(self.totalFolders):
                        new_list = folder.decode_string_to_folders(self.totalFolders)
                        new_list.remove(self.menuItems[0])
                        folder.folders = folder.encode_folders_to_string(new_list)
                        folder.folders = folder.encode_folders_to_string(
                            folder.decode_string_to_folders(self.totalFolders) + [togo])
        else:
            folder = None
            for i in self.totalFolders:
                if i.name == data[4].get():
                    i.folders = i.encode_folders_to_string(i.decode_string_to_folders(self.totalFolders) + [togo])
                    folder = True
            if folder is None:
                self.totalFolders[0].folders = self.totalFolders[0].encode_folders_to_string(
                    self.totalFolders[0].decode_string_to_folders(self.totalFolders) + [togo])

        if remove_old:
            try:
                os.remove(f"Data/Folders/'{self.menuItems[0].name}'.json")
                self.totalFolders.remove(self.menuItems[0])
                print("Old Data removed")
            except FileNotFoundError:
                print("No previous data")

        self.encode_folders()
        self.Set.destroy()
        self.restart()

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
        self.Set.destroy()
        self.restart()

    def restart(self):
        self.root.deiconify()
        self.refresh_menu()

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
                self.Set, ItemDat, FolderDat, Tab = interfaces.add_window(self.Set, self.totalFolders, self.totalItems)
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
            elif command == "~~Reset~~":
                actually_reset = messagebox.askyesno('Confirm',
                                                     f'Are you sure you want to reset your settings to default?')
                if actually_reset:
                    self.reset_settings()
                self.restart()
            elif command == "~~Backup~~":
                tools.backup()
                messagebox.showinfo('Complete', 'All Data Has Been Backed Up')
            elif command == "~~Restore~~":
                if os.path.exists('Backup.zip'):
                    message = f"Are you sure you want to reset your data to the backup's?  "
                    warn = "ALL CHANGES SINCE THIS BACKUP WILL BE OVERRIDDEN"
                    actually_restore = messagebox.askyesno('Confirm', message + warn)
                    if actually_restore:
                        tools.restore()
                        messagebox.showinfo('Complete', 'All Data Has Been Restored')
                        self.restart()
            elif command == "~~Edit_Base~~":
                self.root.withdraw()
                self.Set = Toplevel(self.root)
                self.Set.title("Edit Base")
                self.Set, item_data, folder_data = interfaces.edit_base_window(self.Set, self.totalFolders[0],
                                                                               self.totalFolders, self.totalItems)
                b = Button(self.Set, text="Save",
                           command=lambda data_in=[item_data, folder_data]: self.edit_base_dir(data_in))
                b.pack()
                self.Set = window.center_add_window(self.Set)
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

        else:
            print("Invalid Item")

    # noinspection PyUnusedLocal
    def back(self, event):
        if not self.currentFolder.name == self.basefolder.name:
            self.switch_folder(self.currentFolder.parent)

    def refresh_menu(self):
        for i in self.items:
            if i not in self.totalItems:
                self.items.remove(i)
        for f in self.folders:
            if f not in self.totalFolders:
                self.folders.remove(f)
        if self.currentFolder.name == '0_0Base':
            self.menuItems = self.folders + self.items + [self.systemitems[0]] + [self.settings_folder]
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
        if folder == "System":
            target = self.settings_folder
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
        f.close()
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
        self.settings = classes.Settings('Top', 100, 'unknown.png', 'folder.png', "#d2d2d2", "black", "red", "grey")
        self.restart()


def main():
    ui = GUI()
    ui = interfaces.init_input(ui)
    ui.root.mainloop()


main()
