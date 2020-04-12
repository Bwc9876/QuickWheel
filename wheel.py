from math import sin, cos, radians as rad
from tkinter import Canvas, TclError, PhotoImage, Label

import window


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)


Canvas.create_circle = _create_circle


def render_item_name(can, item, color):
    out = can
    cent = [out.w / 2, out.h / 2]
    out.canvas.create_text(cent[0], cent[1], fill=color, font="Times 50 bold", text=item.name.replace("~", ""))
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


def create_bg(canvas, wheel_color, inner_color):
    out = canvas
    out.canvas.create_circle(canvas.w / 2, canvas.h / 2, canvas.largeCircleSize, outline="#699", width=4,
                             fill=wheel_color)
    out.canvas.create_circle(canvas.w / 2, canvas.h / 2, canvas.smallCircleSize, outline=inner_color, width=4,
                             fill=inner_color)
    return out


def render_cursor(can, direction, color):
    out = can
    s = sin(rad(direction))
    c = cos(rad(direction))
    cent = [out.w / 2, out.h / 2]
    initial_point = [out.w / 2, ((out.h / 2) - out.smallCircleSize) - ((out.largeCircleSize - out.smallCircleSize) / 2)]
    point_a = [initial_point[0] - cent[0], initial_point[1] - cent[1]]
    point_b = [point_a[0] * c - point_a[1] * s, point_a[0] * s + point_a[1] * c]
    point_c = [point_b[0] + cent[0], point_b[1] + cent[1]]
    out.canvas.create_rectangle(point_c[0] - 60, point_c[1] - 75, point_c[0] + 60,
                                point_c[1] + 80, fill=color)
    return out


def render_item(canvas, angle, item, default, default_folder):
    out = canvas
    cent = [out.w / 2, out.h / 2]
    initial_point = [out.w / 2, ((out.h / 2) - out.smallCircleSize) - ((out.largeCircleSize - out.smallCircleSize) / 2)]
    s = sin(rad(angle))
    c = cos(rad(angle))

    if item.what_are_you() == "Item":
        try:
            icon = PhotoImage(file=f'Data/Images/{item.image}')
        except TclError:
            try:
                icon = PhotoImage(file=f'Data/Images/{default}')
            except TclError:
                icon = PhotoImage(file=f'Data/Images/unknown.png')

    else:
        try:
            icon = PhotoImage(file=f'Data/Images/{item.image}')
        except TclError:
            try:
                icon = PhotoImage(file=f'Data/Images/{default_folder}')
            except TclError:
                icon = PhotoImage(file=f'Data/Images/folder.png')

    point_a = [initial_point[0] - cent[0], initial_point[1] - cent[1]]
    point_b = [point_a[0] * c - point_a[1] * s, point_a[0] * s + point_a[1] * c]
    point_c = [point_b[0] + cent[0], point_b[1] + cent[1]]
    label = Label(image=icon)
    label.image = icon
    out.canvas.create_image(point_c[0], point_c[1], image=icon, anchor="center")
    return out


def render_items(can, items, direction, defaults):
    out = can
    interval = 360 / len(items)
    current = direction
    for item in items:
        out = render_item(out, current, item, defaults[0], defaults[1])
        current += interval
    return out


def render_init(master, items, settings):
    directions = {
        'Left': 270,
        'Right': 90,
        'Bottom': 180,
        'Top': 0,
    }
    root, can = create_main_can(master, 1000)
    can = create_bg(can, settings.wheel_color, settings.inner_circle_color)
    can = render_cursor(can, directions[settings.selector_pos], settings.cursor_color)
    can = render_item_name(can, items[0], settings.name_color)
    can = render_items(can, items, directions[settings.selector_pos],
                       [settings.default_icon, settings.default_folder_icon])
    return root, can


def render_refresh(items, canvas, settings):
    directions = {
        'Left': 270,
        'Right': 90,
        'Bottom': 180,
        'Top': 0,
    }
    canvas.canvas.delete("all")
    can = canvas
    can = create_bg(can, settings.wheel_color, settings.inner_circle_color)
    can = render_cursor(can, directions[settings.selector_pos], settings.cursor_color)
    can = render_item_name(can, items[0], settings.name_color)
    can = render_items(can, items, directions[settings.selector_pos],
                       [settings.default_icon, settings.default_folder_icon])
    return can


def init_render(ui):
    ui.root, ui.canvas = render_init(ui.root, ui.menuItems, ui.settings)


def regenerate_canvas(ui):
    ui.root = window.update_window(ui.root, ui.settings)
    render_refresh(ui.menuItems, ui.canvas, ui.settings)
