#!/usr/bin/env python

import argparse
import json

import pyperclip
import tkinter as tk

try:
    import yaml
except ImportError:
    pass


def get_lines(data_file):
    if data_file.endswith(".json"):
        with open(data_file) as jsf:
            data = json.load(jsf)
    elif data_file.endswith(".yml") or data_file.endswith(".yaml"):
        with open(data_file) as ymlf:
            data = yaml.safe_load(ymlf)
    else:
        with open(data_file) as text:
            data = {f"Line {i}": line.strip() for i, line in enumerate(text, start=1)}

    for key, value in data.items():
        yield key, value


# define button click handler function
def handle_click(key, label):
    pyperclip.copy(label)
    print(f"Copied '{key}': {label}")


parser = argparse.ArgumentParser()
parser.add_argument("data_file")
args = parser.parse_args()


# create Tkinter window
root = tk.Tk()
root.title("Clipboard dial")

# create buttons with labels from text file
for key, label in get_lines(args.data_file):
    tk.Label(root, text=key).pack()
    button = tk.Button(
        root, text=label, command=lambda key=key, label=label: handle_click(key, label)
    )
    button.pack()

# set "always on top" attribute
root.attributes("-topmost", True)

# start Tkinter event loop
root.mainloop()
