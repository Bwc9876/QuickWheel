def center(tk, can):
    out = tk
    window_width = can.w
    window_height = can.h
    position_right = int(out.winfo_screenwidth() / 2 - window_width / 2)
    position_down = int(out.winfo_screenheight() / 2 - window_height / 2)
    out.geometry("+{}+{}".format(position_right, position_down))
    return out


def center_add_window(tk):
    out = tk
    window_width = out.winfo_reqwidth()
    window_height = out.winfo_reqheight()
    position_right = int(out.winfo_screenwidth() / 2 - window_width / 2)
    position_down = int(out.winfo_screenheight() / 2 - window_height / 2)
    out.geometry("+{}+{}".format(position_right, position_down))
    return out


def override_other_windows(tk):
    root = tk
    root.overrideredirect(True)
    root.wm_attributes("-topmost", 1)
    return root


def initialize_window(tk, can):
    root = tk
    root = center(root, can)
    root = override_other_windows(root)
    root.wm_attributes("-transparentcolor", "#699")
    return root
