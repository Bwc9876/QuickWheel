import core
import wheel


# noinspection PyUnusedLocal,PyDefaultArgument
class Ui:

    def __init__(self):
        self.items = []
        self.folders = []
        self.root = None
        self.Set = None
        self.canvas = None
        self.folders = []
        self.settings_folder = None
        self.currentFolder = None
        self.systemitems = []
        self.basefolder = None
        self.totalItems = None
        self.totalFolders = None
        self.menuItems = []
        self.commands = {}

    def exit(self, event):
        self.root.destroy()

    def exit_no_event(self):
        self.root.destroy()

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
        wheel.regenerate_canvas(self)

    def restart(self):
        self.root.deiconify()
        self.refresh_menu()


def main():
    ui = Ui()
    core.initialize(ui)
    ui.root.mainloop()


main()
