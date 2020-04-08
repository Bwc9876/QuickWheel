import json
from json import JSONEncoder


class Item:
    def __init__(self, name, img, command, data=None):
        if data is None:
            self.name = name
            self.image = img
            self.command = command
        else:
            self.__dict__ = json.loads(data)

    def __str__(self):
        return self.name

    @staticmethod
    def what_are_you():
        return "Item"


class ItemEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class Folder:
    def __init__(self, name, parent, icon, items, folders, data=None):
        if data is None:
            self.name = name
            self.parent = parent
            self.image = icon
            self.items = items
            self.folders = folders
        else:
            self.__dict__ = json.loads(data)

    def __str__(self):
        return self.name

    @staticmethod
    def what_are_you():
        return "Folder"

    @staticmethod
    def encode_items_to_string(item_list):
        out = ''
        for i in item_list:
            out += i.name
            out += '~'
        return out[:-1]

    def decode_string_to_items(self, total):
        out = []
        for i in self.items.split('~'):
            for n in total:
                if i == n.name:
                    out += [n]
        return out

    @staticmethod
    def encode_folders_to_string(item_list):
        out = ''
        for i in item_list:
            out += i.name
            out += '~'
        return out[:-1]

    def decode_string_to_folders(self, total):
        out = []
        for i in self.folders.split('~'):
            for n in total:
                if i == n.name:
                    out += [n]
        return out


class FolderEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
