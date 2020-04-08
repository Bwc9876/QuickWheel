from math import sin, cos, radians as rad
from tkinter import *


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)


Canvas.create_circle = _create_circle


def render_item_name(can, item):
    out = can
    cent = [out.w / 2, out.h / 2]
    out.canvas.create_text(cent[0], cent[1], fill="red", font="Times 50 bold", text=item.name.replace("~", ""))
    return out


class MainCan:
    def __init__(self, w, h, bg, master):
        self.w = w
        self.h = h
        self.bg = bg
        self.largeCircleSize = (w - 10) / 2
        self.smallCircleSize = (w - 300) / 2
        self.canvas = Canvas(master, width=w, height=h, borderwidth=0, highlightthickness=0, bg=bg)


def create_main_can(master, size):
    root = master
    canvas = MainCan(size, size, '#699', root)
    canvas.canvas.grid()
    return root, canvas


def create_bg(canvas):
    out = canvas
    out.canvas.create_circle(canvas.w / 2, canvas.h / 2, canvas.largeCircleSize, outline="#DDD", width=4, fill="#DDD")
    out.canvas.create_circle(canvas.w / 2, canvas.h / 2, canvas.smallCircleSize, outline="#DDD", width=4, fill="black")
    return out


def render_cursor(can):
    out = can
    initial_point = [out.w / 2, ((out.h / 2) - out.smallCircleSize) - ((out.largeCircleSize - out.smallCircleSize) / 2)]
    out.canvas.create_rectangle(initial_point[0] - 60, initial_point[1] - 75, initial_point[0] + 60,
                                initial_point[1] + 80, fill="grey")
    return out


def render_item(canvas, angle, item):
    out = canvas
    cent = [out.w / 2, out.h / 2]
    initial_point = [out.w / 2, ((out.h / 2) - out.smallCircleSize) - ((out.largeCircleSize - out.smallCircleSize) / 2)]
    s = sin(rad(angle))
    c = cos(rad(angle))

    if item.what_are_you() == "Item":
        try:
            icon = PhotoImage(file=f'Images/{item.image}')
        except FileNotFoundError:
            icon = PhotoImage(file=f'Images/unknown.png')
    else:
        try:
            icon = PhotoImage(file=f'Images/{item.image}')
        except FileNotFoundError:
            icon = PhotoImage(file=f'Images/folder.png')

    point_a = [initial_point[0] - cent[0], initial_point[1] - cent[1]]
    point_b = [point_a[0] * c - point_a[1] * s, point_a[0] * s + point_a[1] * c]
    point_c = [point_b[0] + cent[0], point_b[1] + cent[1]]
    label = Label(image=icon)
    label.image = icon
    out.canvas.create_image(point_c[0], point_c[1], image=icon, anchor="center")
    return out


def render_items(can, items):
    out = can
    interval = 360 / len(items)
    current = 0
    for item in items:
        out = render_item(out, current, item)
        current += interval
    return out


def render_init(master, items):
    root, can = create_main_can(master, 1000)
    can = create_bg(can)
    can = render_cursor(can)
    can = render_item_name(can, items[0])
    can = render_items(can, items)
    return root, can


def render_refresh(items, canvas):
    canvas.canvas.delete("all")
    can = canvas
    can = create_bg(can)
    can = render_cursor(can)
    can = render_item_name(can, items[0])
    can = render_items(can, items)
    return can
