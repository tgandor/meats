#!/usr/bin/env python

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
import os

def play(url_entry):
    print(url_entry.get())
    urls = os.popen('youtube-dl -g '+url_entry.get()).readlines()
    print(urls)
    if len(urls) == 1:
        os.system('mplayer -vf crop=900:500:0:220 "{}"'.format(urls[0].strip()))
    else:
        os.system('mplayer -vf crop=900:500:0:220 "{}" -audiofile "{}"'.format(*[u.strip() for u in urls]))


root = tk.Tk()
root.title("Crop watch URL")
#root.geometry("600x50")

url = tk.Entry(root, width=80)
url.pack(anchor=tk.N)

watch = tk.Button(root, text='Watch', command=lambda: play(url), width=80)
watch.pack(anchor=tk.N)

root.mainloop()

