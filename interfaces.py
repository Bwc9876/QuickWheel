from tkinter import *
from tkinter import ttk


def item(tk, item_tab):
    n = Label(item_tab, text="Name")
    n.pack(side=TOP)
    w = Entry(item_tab)
    w.pack(side=TOP)
    i = Label(item_tab, text="Image Name")
    i.pack(side=TOP)
    f = Entry(item_tab)
    f.pack(side=TOP)
    c = Label(item_tab, text="Command")
    c.pack(side=TOP)
    t = Entry(item_tab)
    t.pack(side=TOP)
    p = Label(item_tab, text="Folder (Leave blank for root)")
    p.pack(side=TOP)
    y = Entry(item_tab)
    y.pack(side=TOP)
    return tk, w, f, t, y


def folder(tk, folder_tab):
    n = Label(folder_tab, text="Name")
    n.pack(side=TOP)
    w = Entry(folder_tab)
    w.pack(side=TOP)
    i = Label(folder_tab, text="Image Name")
    i.pack(side=TOP)
    f = Entry(folder_tab)
    f.pack(side=TOP)
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
    return tk, w, f, t, y, g


def add_window(tk):
    tab_control = ttk.Notebook(tk)
    item_tab = ttk.Frame(tab_control)
    folder_tab = ttk.Frame(tab_control)
    tab_control.add(item_tab, text="Item")
    tab_control.add(folder_tab, text="Folder")
    tab_control.pack(expand=1, fill="both")
    tk, w, f, t, y = item(tk, item_tab)
    tk, w1, f1, t1, y1, g = folder(tk, folder_tab)
    item_data = [w, f, t, y]
    folder_data = [w1, f1, t1, y1, g]
    return tk, item_data, folder_data, tab_control


def init_input(ui):
    ui.root.bind('<Right>', ui.right)
    ui.root.bind('<Left>', ui.left)
    ui.root.bind('<a>', ui.left)
    ui.root.bind('<d>', ui.right)
    ui.root.bind('<Escape>', ui.exit)
    ui.root.bind('<Return>', ui.invoke)
    ui.root.bind('<w>', ui.invoke)
    ui.root.bind('<Up>', ui.invoke)
    ui.root.bind('<Down>', ui.back)
    ui.root.bind('<s>', ui.back)
    return ui
