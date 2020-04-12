from tkinter import Toplevel, Button, BOTTOM, messagebox, Tk

import actions
import constants
import data
import delete
import dialogue
import folder
import input
import item
import settings
import wheel
import window


# noinspection PyUnusedLocal
def debug(ui, args):
    print("Dummy command triggered")


# noinspection PyUnusedLocal
def invoke(ui, event):
    what = ui.menuItems[0]
    if what.what_are_you() == "Item":
        commands = {
            "~~Exit~~": stop,
            "~~Add~~": add_event,
            "~~Back~~": folder.back_no_event,
            "~~Set~~": settings_window,
            "~~Dummy~~": debug,
            "~~Reset~~": settings.ask_reset_settings,
            "~~Backup~~": data.backup_event,
            "~~Restore~~": data.confirm_restore,
            "~~Edit_Base~~": folder.edit_base,
            "launch": actions.open_app,
            "open": actions.open_file,
            "openwith": actions.open_file_with,
            "run": actions.run,
            "web": actions.web,
        }
        try:
            if what.command in constants.meta_commands:
                commands[what.command](ui, what.args)
            elif what.command in ui.user_commands:
                commands[what.command](what.args)
                ui.exit_no_event("Exiting...")
        except KeyError:
            messagebox.showinfo('Unable to run', "This item's command is not recognized")
    elif what.what_are_you() == "Folder":
        folder.switch_folder(ui, what.name)
    else:
        messagebox.showinfo('Unable to run', 'This item is corrupted')


def initialize(ui):
    ui.root = Tk()
    init_input(ui)
    folder.initialize_system_folder(ui)
    folder.initialize_user_folders(ui)
    item.initialize_user_items(ui)
    item.setup_system_items(ui)
    settings.initialize_settings(ui)
    ui.menuItems = ui.folders + ui.items + [ui.systemitems[0]] + [ui.settings_folder]
    wheel.init_render(ui)
    window.init_window(ui)


# noinspection PyUnusedLocal
def stop(ui, event):
    ui.root.destroy()


# noinspection PyUnusedLocal
def edit_selected(ui, event):
    if ui.menuItems[0].name not in constants.non_editable:
        old_item = ui.menuItems[0]
        ui.root.withdraw()
        ui.Set = Toplevel(ui.root)
        ui.Set.title(f"Edit {old_item.name}")
        ui.Set, dat = dialogue.edit_window(ui.Set, old_item, ui.totalFolders, ui.totalItems,
                                           constants.user_commands)
        if old_item.what_are_you() == "Item":
            b = Button(ui.Set, text=f"Save {old_item.name}",
                       command=lambda data_in=dat: item.add_item(ui, data_in, remove_old=True))
            b.pack()
        elif old_item.what_are_you() == "Folder":
            b = Button(ui.Set, text=f"Save {old_item.name}",
                       command=lambda data_in=dat: folder.add_folder(ui, data_in, remove_old=True))
            b.pack()
        ui.Set = window.center_add_window(ui.Set)


def add(ui, data_in):
    what = data_in[2].tab(data_in[2].select(), 'text')
    if what == "Item":
        item.add_item(ui, data_in[0])
    else:
        folder.add_folder(ui, data_in[1])


# noinspection PyDefaultArgument,PyUnusedLocal
def add_event(ui, args):
    ui.root.withdraw()
    ui.Set = Toplevel(ui.root)
    ui.Set.title("Add...")
    ui.Set, ItemDat, FolderDat, Tab = dialogue.add_window(ui.Set, ui.totalFolders, ui.totalItems,
                                                          constants.user_commands)
    b = Button(ui.Set, text="Save", command=lambda data_in=[ItemDat, FolderDat, Tab]: add(ui, data_in))
    b.pack()
    ui.Set = window.center_add_window(ui.Set)


# noinspection PyUnusedLocal
def settings_window(ui, args):
    ui.root.withdraw()
    ui.Set = Toplevel(ui.root)
    ui.Set.title("Settings")
    ui.Set, data_in = dialogue.edit_settings(ui.Set, ui.settings)
    b = Button(ui.Set, text="Save", command=lambda data_1=data_in: settings.save_settings(ui, data_1))
    b.pack(side=BOTTOM)
    ui.Set = window.center_add_window(ui.Set)


def init_input(ui):
    ui.root.bind('<Right>', lambda event, direction=1: input.direction_handler(ui, event, direction))
    ui.root.bind('<Left>', lambda event, direction=0: input.direction_handler(ui, event, direction))
    ui.root.bind('<a>', lambda event, direction=0: input.direction_handler(ui, event, direction))
    ui.root.bind('<d>', lambda event, direction=1: input.direction_handler(ui, event, direction))
    ui.root.bind('<Escape>', lambda event, ui_in=ui: stop(ui, event))
    ui.root.bind('<e>', lambda event, ui_in=ui: edit_selected(ui_in, event))
    ui.root.bind('<q>', lambda event, ui_in=ui: delete.delete_event(ui, event))
    ui.root.bind('<Return>', lambda event, ui_in=ui: invoke(ui, event))
    ui.root.bind('<w>', lambda event, ui_in=ui: invoke(ui, event))
    ui.root.bind('<Up>', lambda event, ui_in=ui: invoke(ui, event))
    ui.root.bind('<Down>', lambda event, ui_in=ui: folder.back(ui, event))
    ui.root.bind('<s>', lambda event, ui_in=ui: folder.back(ui, event))
    return ui
