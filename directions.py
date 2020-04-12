from collections import deque

import wheel


def right(ui):
    item_out = deque(ui.menuItems)
    item_out.rotate(-1)
    ui.menuItems = list(item_out)
    wheel.regenerate_canvas(ui)


def left(ui):
    item_out = deque(ui.menuItems)
    item_out.rotate(1)
    ui.menuItems = list(item_out)
    wheel.regenerate_canvas(ui)


# noinspection PyUnusedLocal
def direction_handler(ui, event, input_direction):
    positions = {
        'Top': [left, right],
        'Bottom': [right, left],
    }
    positions[ui.settings.selector_pos][input_direction](ui)
