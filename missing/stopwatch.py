#!/usr/bin/env python

import os
import sys
import time

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import tkMessageBox as messagebox
except ImportError:
    from tkinter import messagebox

def to_hms(seconds):
    h, s = divmod(seconds, 3600)
    m, s = divmod(s, 60)
    return '{0:02.0f}:{1:02.0f}:{2:04.1f}'.format(int(h), m, s)

class StopWatchDialog(tk.Frame):
    STATE_IDLE = 0
    STATE_RUNNING = 1
    STATE_STOPPED = 2

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.elapsed_time = 0
        self.start_time = None
        self.state = self.STATE_IDLE
        self.initUI()
        self.update_elapsed()

    def initUI(self):
        self.parent.title("stopper")
        self.pack(fill=tk.BOTH, expand=1)

        self.parent.bind("<Escape>", lambda event: self.parent.destroy())

        self.startButton = tk.Button(self, text="Start", command=self.start,
                                        width=18)
        self.startButton.pack()

        self.elapsed = tk.Label(self, text="")
        self.elapsed.pack()

        self.stopButton = tk.Button(self, text="Stop", command=self.stop,
                                    width=18, state=tk.DISABLED)
        self.stopButton.pack()

        #self.statusLabel = tk.Label(self, text="Idle")
        #self.statusLabel.pack()

        self.startButton.focus_set()

    def update_elapsed(self):
        self.elapsed.config(text=to_hms(self.elapsed_time))

    def cycle(self):
        if self.state == self.STATE_STOPPED:
            return
        self.elapsed_time = time.time() - self.start_time
        self.update_elapsed()
        self.after(100, self.cycle)

    def start(self):
        self.start_time = time.time()
        self.state = self.STATE_RUNNING
        self.after(100, self.cycle)
        self.startButton.config(text="Restart")
        self.stopButton.config(state=tk.NORMAL)
        self.stopButton.focus_set()

    def stop(self):
        self.elapsed_time = time.time() - self.start_time
        self.state = self.STATE_STOPPED
        self.update_elapsed()
        self.stopButton.config(state=tk.DISABLED)
        self.startButton.focus_set()


root = tk.Tk()
ex = StopWatchDialog(root)
root.geometry("+300+300")
root.mainloop()

