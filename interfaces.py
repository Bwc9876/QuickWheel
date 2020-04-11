from tkinter import Label, OptionMenu, Spinbox, StringVar, BooleanVar, TOP, Entry, Button, Checkbutton, IntVar
from tkinter import colorchooser
from tkinter import filedialog
from tkinter import ttk

from tools import convert_items_to_dict


def choose_file_image(temp, mode):
    out = filedialog.askopenfilename(title="Select Image", filetypes=(("png files", "*.png"),))
    if mode == "default_icon":
        temp.default_icon = out
    elif mode == "default_folder":
        temp.default_folder = out
    elif mode == "icon" or mode == "folder":
        temp.image = out


class TempAddData:
    def __init__(self):
        self.image = None


def item(tk, item_tab, folders):
    temp_item = TempAddData()
    n = Label(item_tab, text="Name")
    n.pack(side=TOP)
    w = Entry(item_tab)
    w.pack(side=TOP)
    i = Label(item_tab, text="Image")
    i.pack(side=TOP)
    icon_file_button = Button(item_tab, text="Choose File",
                              command=lambda temp=temp_item: choose_file_image(temp, "icon"))
    icon_file_button.pack()
    c = Label(item_tab, text="Command")
    c.pack(side=TOP)
    t = Entry(item_tab)
    t.pack(side=TOP)
    p = Label(item_tab, text="Folder (Base is top level)")
    p.pack(side=TOP)
    parent = StringVar()
    parent_choices = []
    for i in folders:
        parent_choices += [i.name.replace('0_0', '')]
    parent.set(parent_choices[0])
    parent_drop = OptionMenu(item_tab, parent, *parent_choices)
    parent_drop.pack()
    return tk, w, temp_item, t, parent


def folder(tk, folder_tab, folders, items):
    temp_folder = TempAddData()
    n = Label(folder_tab, text="Name")
    n.pack(side=TOP)
    w = Entry(folder_tab)
    w.pack(side=TOP)
    i = Label(folder_tab, text="Image")
    i.pack(side=TOP)
    icon_file_button = Button(folder_tab, text="Choose File",
                              command=lambda temp=temp_folder: choose_file_image(temp, "folder"))
    icon_file_button.pack()
    c = Label(folder_tab, text="Items")
    c.pack(side=TOP)
    item_dict = {}
    if len(items) == 0:
        p = Label(folder_tab, text="No Already Made Items", font='Helvetica 10 bold')
        p.pack(side=TOP)
    for i in items:
        if not i.name == "0_0Base":
            item_dict[i.name] = BooleanVar()
            box = Checkbutton(folder_tab, text=i.name, var=item_dict[i.name])
            box.pack()
    p = Label(folder_tab, text="Folders")
    p.pack(side=TOP)
    folder_dict = {}
    if len(folders) - 1 == 0:
        j = Label(folder_tab, text="No Already Made Folders", font='Helvetica 10 bold')
        j.pack(side=TOP, pady=5)
    for i in folders:
        if not i.name == "0_0Base":
            folder_dict[i.name] = BooleanVar()
            box = Checkbutton(folder_tab, text=i.name, var=folder_dict[i.name])
            box.pack()
    u = Label(folder_tab, text="Parent Folder (Base is top level)")
    u.pack(side=TOP)
    parent = StringVar()
    parent_choices = []
    for i in folders:
        parent_choices += [i.name.replace('0_0', '')]
    parent.set(parent_choices[0])
    parent_drop = OptionMenu(folder_tab, parent, *parent_choices)
    parent_drop.pack()
    return tk, w, temp_folder, item_dict, folder_dict, parent


def add_window(tk, folders, items):
    tab_control = ttk.Notebook(tk)
    item_tab = ttk.Frame(tab_control)
    folder_tab = ttk.Frame(tab_control)
    tab_control.add(item_tab, text="Item")
    tab_control.add(folder_tab, text="Folder")
    tab_control.pack(expand=1, fill="both")
    tk, w, item_temp, t, y = item(tk, item_tab, folders)
    tk, w1, folder_temp, t1, y1, g = folder(tk, folder_tab, folders, items)
    item_data = [w, item_temp, t, y]
    folder_data = [w1, folder_temp, t1, y1, g]
    return tk, item_data, folder_data, tab_control


def edit_base_window(tk, in_base, folders, items):
    c = Label(tk, text="Items")
    c.pack(side=TOP)
    temp_dict = convert_items_to_dict(in_base.items, items)
    new_item_dict = {}
    if len(items) == 0:
        p = Label(tk, text="No Already Made Items", font='Helvetica 10 bold')
        p.pack(side=TOP)
    for item_iterator in temp_dict:
        new_item_dict[item_iterator] = BooleanVar()
        new_item_dict[item_iterator].set(temp_dict[item_iterator])
        box = Checkbutton(tk, text=item_iterator, var=new_item_dict[item_iterator])
        box.pack()

    p = Label(tk, text="Folders")
    p.pack(side=TOP)

    temp_folder_dict = convert_items_to_dict(in_base.folders, folders)
    new_folder_dict = {}
    if len(folders) - 1 == 0:
        j = Label(tk, text="No Already Made Folders", font='Helvetica 10 bold')
        j.pack(side=TOP, pady=5)
    for fold in temp_folder_dict:
        new_folder_dict[fold] = BooleanVar()
        new_folder_dict[fold].set(temp_folder_dict[fold])
        box = Checkbutton(tk, text=fold, var=new_folder_dict[fold])
        box.pack()
    return tk, new_item_dict, new_folder_dict


def edit_window(tk, item_in, folders, items):
    if item_in.what_are_you() == "Folder":
        temp_folder = TempAddData()
        n = Label(tk, text="Name")
        n.pack(side=TOP)
        w = Entry(tk)
        w.insert(0, item_in.name)
        w.pack(side=TOP)
        i = Label(tk, text="Image")
        i.pack(side=TOP)
        icon_file_button = Button(tk, text="Choose File",
                                  command=lambda temp=temp_folder: choose_file_image(temp, "folder"))
        icon_file_button.pack()
        c = Label(tk, text="Items")
        c.pack(side=TOP)
        temp_dict = convert_items_to_dict(item_in.items, items)
        new_item_dict = {}
        if len(items) == 0:
            p = Label(tk, text="No Already Made Items", font='Helvetica 10 bold')
            p.pack(side=TOP)
        for item_iterator in temp_dict:
            new_item_dict[item_iterator] = BooleanVar()
            new_item_dict[item_iterator].set(temp_dict[item_iterator])
            box = Checkbutton(tk, text=item_iterator, var=new_item_dict[item_iterator])
            box.pack()

        p = Label(tk, text="Folders")
        p.pack(side=TOP)

        temp_folder_dict = convert_items_to_dict(item_in.folders, folders)
        new_folder_dict = {}
        if len(folders) - 1 == 0:
            j = Label(tk, text="No Already Made Folders", font='Helvetica 10 bold')
            j.pack(side=TOP, pady=5)
        for fold in temp_folder_dict:
            new_folder_dict[fold] = BooleanVar()
            new_folder_dict[fold].set(temp_folder_dict[fold])
            box = Checkbutton(tk, text=fold, var=new_folder_dict[fold])
            box.pack()

        return tk, [w, temp_folder, new_item_dict, new_folder_dict, "noedit"]
    elif item_in.what_are_you() == "Item":
        temp_item = TempAddData()
        n = Label(tk, text="Name")
        n.pack(side=TOP)
        w = Entry(tk)
        w.insert(0, item_in.name)
        w.pack(side=TOP)
        i = Label(tk, text="Image")
        i.pack(side=TOP)
        icon_file_button = Button(tk, text="Choose File",
                                  command=lambda temp=temp_item: choose_file_image(temp, "icon"))
        icon_file_button.pack()
        c = Label(tk, text="Command")
        c.pack(side=TOP)
        t = Entry(tk)
        t.insert(0, item_in.command)
        t.pack(side=TOP)
        return tk, [w, temp_item, t, "noedit"]
    return None


class TempSettingsData:
    def __init__(self):
        self.default_icon = None
        self.default_folder = None
        self.wheel_color = None
        self.inner_color = None
        self.name_color = None
        self.cursor_color = None


def choose_color(temp, mode):
    out = colorchooser.askcolor()
    if mode == "wheel":
        temp.wheel_color = out[1]
    elif mode == "inner":
        temp.inner_color = out[1]
    elif mode == "name":
        temp.name_color = out[1]
    elif mode == "cursor":
        temp.cursor_color = out[1]


def edit_settings(tk, settings):
    temporary_settings = TempSettingsData()
    padding = 5

    # Start Selector Position
    n = Label(tk, text="Cursor Position")
    n.pack(side=TOP)
    pos = StringVar()
    pos_choices = {'Top', 'Bottom'}
    pos.set(settings.selector_pos)
    position_drop = OptionMenu(tk, pos, *pos_choices)
    position_drop.pack(pady=padding)
    # End Selector Position

    # Start Transparency
    i = Label(tk, text="Transparency (10 is nearly invisible, 100 is solid)")
    i.pack(side=TOP)
    trans = IntVar()
    trans.set(settings.transparency)
    transparency_spinbox = Spinbox(tk, from_=10, to=100, width=5, textvariable=trans)
    transparency_spinbox.pack(pady=padding)
    # End Transparency

    # Start default_icon
    icon_file_button = Button(tk, text="Choose Default Icon Image File",
                              command=lambda temp=temporary_settings: choose_file_image(temp, "default_icon"))
    icon_file_button.pack(pady=padding)
    # End default_icon

    # Start default_folder_icon
    folder_file_button = Button(tk, text="Choose Default Folder Image File",
                                command=lambda temp=temporary_settings: choose_file_image(temp, "default_folder"))
    folder_file_button.pack(pady=padding)
    # End default_folder_icon

    # Start wheel_color
    wheel_color_button = Button(tk, text="Choose Wheel Color",
                                command=lambda temp=temporary_settings: choose_color(temp, "wheel"))
    wheel_color_button.pack(pady=padding)
    # End wheel_color

    # Start inner_color
    inner_color_button = Button(tk, text="Choose Inner Wheel Color",
                                command=lambda temp=temporary_settings: choose_color(temp, "inner"))
    inner_color_button.pack(pady=padding)
    # End inner_color

    # Start text_color
    name_color_button = Button(tk, text="Choose Name Color",
                               command=lambda temp=temporary_settings: choose_color(temp, "name"))
    name_color_button.pack(pady=padding)
    # End text_color

    # Start cursor_color
    cursor_color_button = Button(tk, text="Choose Cursor Color",
                                 command=lambda temp=temporary_settings: choose_color(temp, "cursor"))
    cursor_color_button.pack(pady=(padding, 16))
    # End cursor_color

    # Start Output
    return tk, [pos, trans, temporary_settings]
    # End Output


def init_input(ui):
    ui.root.bind('<Right>', lambda event, direction=1: ui.direction_handler(event, direction))
    ui.root.bind('<Left>', lambda event, direction=0: ui.direction_handler(event, direction))
    ui.root.bind('<a>', lambda event, direction=0: ui.direction_handler(event, direction))
    ui.root.bind('<d>', lambda event, direction=1: ui.direction_handler(event, direction))
    ui.root.bind('<Escape>', ui.exit)
    ui.root.bind('<e>', ui.edit_selected)
    ui.root.bind('<q>', ui.delete)
    ui.root.bind('<Return>', ui.invoke)
    ui.root.bind('<w>', ui.invoke)
    ui.root.bind('<Up>', ui.invoke)
    ui.root.bind('<Down>', ui.back)
    ui.root.bind('<s>', ui.back)
    return ui
