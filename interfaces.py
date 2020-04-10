from tkinter import *
from tkinter import colorchooser
from tkinter import filedialog
from tkinter import ttk


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


def item(tk, item_tab):
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
    p = Label(item_tab, text="Folder (Leave blank for root)")
    p.pack(side=TOP)
    y = Entry(item_tab)
    y.pack(side=TOP)
    return tk, w, temp_item, t, y


def folder(tk, folder_tab):
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
    c = Label(folder_tab, text="Items (Separated by ~)")
    c.pack(side=TOP)
    t = Entry(folder_tab)
    t.pack(side=TOP)
    p = Label(folder_tab, text="Folders (Separated by ~)")
    p.pack(side=TOP)
    y = Entry(folder_tab)
    y.pack(side=TOP)
    u = Label(folder_tab, text="Parent Folder (Leave Blank for root)")
    u.pack(side=TOP)
    g = Entry(folder_tab)
    g.pack(side=TOP)
    return tk, w, temp_folder, t, y, g


def add_window(tk):
    tab_control = ttk.Notebook(tk)
    item_tab = ttk.Frame(tab_control)
    folder_tab = ttk.Frame(tab_control)
    tab_control.add(item_tab, text="Item")
    tab_control.add(folder_tab, text="Folder")
    tab_control.pack(expand=1, fill="both")
    tk, w, item_temp, t, y = item(tk, item_tab)
    tk, w1, folder_temp, t1, y1, g = folder(tk, folder_tab)
    item_data = [w, item_temp, t, y]
    folder_data = [w1, folder_temp, t1, y1, g]
    return tk, item_data, folder_data, tab_control


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
    ui.root.bind('<Return>', ui.invoke)
    ui.root.bind('<w>', ui.invoke)
    ui.root.bind('<Up>', ui.invoke)
    ui.root.bind('<Down>', ui.back)
    ui.root.bind('<s>', ui.back)
    return ui
