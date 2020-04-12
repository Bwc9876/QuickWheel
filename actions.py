import os
import webbrowser


def open_app(arg):
    os.startfile(arg)


def open_file(arg):
    os.startfile(arg)


def open_file_with(args):
    os.system(rf'{args.split("~")[0]} {args.split("~")[1]}')


def run(args):
    command = ''
    first = True
    for i in args.split("~"):
        command += i
        if not first:
            command += ' '
        else:
            first = False
    os.system(command)


def web(url):
    webbrowser.open(url, new=2)
