#!/usr/bin/env python

import os
import threading

try:
    import Tkinter as tk
except ImportError:
    os.system('sudo apt-get install python-tk')
    print('Please re-run to use Tkinter')
    exit()

from Tkinter import Frame, Tk, Button, BOTH, Label, Entry, StringVar, Spinbox, NORMAL, DISABLED
import tkMessageBox

try:
    import sane
except ImportError:
    os.system('sudo apt-get install sane sane-utils python-imaging-sane')
    print('Please re-run to use sane scanners')
    exit()

import sane
print 'SANE version:', sane.init()

available = sane.get_devices()
print 'Available devices =', available

if not available:
    print "NO DEVICES FOUND."
    s = None
else:
    s = sane.open(available[0][0])
    s.mode = 'color'


class Settings(object):
    def __init__(self, tk_root):
        self.width = 210.0
        self.height = 297.0
        self.scale = tk.DoubleVar(tk_root, value=1.0)
        self.extension = tk.StringVar(tk_root, value='.png')

    def br_x(self):
        return self.width * self.scale.get()

    def br_y(self):
        return self.height * self.scale.get()

    def ext(self):
        return self.extension.get()


def do_scan(output_filename, settings):
    s.br_x = settings.br_x()
    s.br_y = settings.br_y()
    print 'Resolution: {0}'.format(s.resolution)
    print 'Scanning with parameters:', s.get_parameters()
    s.start()
    print 'started'
    im = s.snap()
    print 'snapped'
    im.save(output_filename)
    return im


class ScanWorker(threading.Thread):
    def __init__(self, output_filename, settings):
        super(ScanWorker, self).__init__()
        self.output_filename = output_filename
        self.settings = settings

    def run(self):
        do_scan(self.output_filename, self.settings)


class ScanDialog(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.worker = None
        self.elapsed = 0
        self.settings = Settings(self)

        # self.initUI() follows

        self.parent.title("Scan Images")
        self.pack(fill=BOTH, expand=1)

        r = 0  # current grid row

        Label(self, text="Name prefix:").grid(row=r, column=0)
        Label(self, text="Number suffix:").grid(row=r, column=1)
        r += 1

        self.newName = StringVar()
        self.newName.set('Scan_')
        newName = Entry(self, textvariable=self.newName, width=60)
        newName.grid(row=1, column=0)
        newName.bind("<Return>",   lambda event: self.scan())
        newName.bind("<KP_Enter>", lambda event: self.scan())
        newName.bind("<Escape>", lambda event: self.parent.destroy())
        newName.focus_set()
        self.newNameEntry = newName

        self.numberSuffix = Spinbox(self, from_=1, to=999)
        self.numberSuffix.bind("<Return>",   lambda event: self.scan())
        self.numberSuffix.bind("<KP_Enter>", lambda event: self.scan())
        self.numberSuffix.grid(row=r, column=1)
        r += 1

        self.okButton = Button(self, text="Scan", command=self.scan, width=60, height=5)
        self.okButton.grid(row=r, column=0)

        cancelButton = Button(self, text="Cancel", command=self.parent.destroy)
        cancelButton.grid(row=r, column=1)
        r += 1

        panel = tk.Frame(self)
        tk.Label(panel, text="Paper Format").pack()
        tk.Radiobutton(panel, text="A4", value=1.0, variable=self.settings.scale).pack()
        tk.Radiobutton(panel, text="A5", value=2 ** (-0.5), variable=self.settings.scale).pack()
        tk.Radiobutton(panel, text="A6", value=0.5, variable=self.settings.scale).pack()
        panel.grid(row=r, column=0)

        panel = tk.Frame(self)
        tk.Label(panel, text="File Format").pack()
        tk.Radiobutton(panel, text="PNG", value='.png', variable=self.settings.extension).pack()
        tk.Radiobutton(panel, text="JPG", value='.jpg', variable=self.settings.extension).pack()
        panel.grid(row=r, column=1)

        r += 1

        self.statusLabel = Label(self, text="Idle")
        self.statusLabel.grid(row=r, column=0, columnspan=2)

    def _checkAlive(self):
        if self.worker is None:
            return
        if self.worker.is_alive():
            self.after(100, self._checkAlive)
            self.elapsed += 1
            self.statusLabel.config(text='Scanning, please wait... (%.1f s)' % (self.elapsed/10.0))
        else:
            self.worker = None
            self.okButton.config(state=NORMAL)
            self.numberSuffix.invoke('buttonup')
            self.newNameEntry.focus_set()
            self.statusLabel.config(text='Idle (last scan: %.1f s)' % (self.elapsed/10.0))

    def _ext(self):
        return self.settings.ext()

    def scan(self):
        target = '%s%03d%s' % (self.newName.get(), int(self.numberSuffix.get()), self._ext(), )
        if os.path.exists(target):
            if not tkMessageBox.askokcancel(title='Scan Images', message='File exists. Overwrite?'):
                print 'Not scanning: %s - file exists!' % target
                new_name = self.newName.get()
                for i in xrange(int(self.numberSuffix.get()), 1000):
                    new_target = '%s%03d.%s' % (new_name, int(self.numberSuffix.get()), self._ext(), )
                    if not os.path.exists(new_target):
                        print 'Next available filename: %s' % (new_target, )
                        self.numberSuffix.delete(0, 'end')
                        self.numberSuffix.insert(0, i)
                        break
                return

        print "Scanning to filename '%s' ..." % (target, )

        if s is None:
            print('No scanner present. Connect and restart application.')
            return

        if self.worker is None:
            self.worker = ScanWorker(target, self.settings)
            self.worker.start()
            self.elapsed = 0
            self.after(100, self._checkAlive)
            self.okButton.config(state=DISABLED)
            self.statusLabel.config(text='Scanning, please wait...')
        else:
            print "Error - not started, worker exists."


root = Tk()
ex = ScanDialog(root)
# root.geometry("650x100+300+300")
root.geometry("+300+300")
root.mainloop()

