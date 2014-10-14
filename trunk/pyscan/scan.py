#!/usr/bin/env python

import os
import sys
import threading

from Tkinter import Frame, Tk, Button, BOTH, Label, Entry, StringVar, END, Spinbox, NORMAL, DISABLED

import sane
print 'SANE version:', sane.init()

available = sane.get_devices()
print 'Available devices=', available

if not available:
    print "NO DEVICES FOUND. File '%s' not saved..." % (output_filename, )
    exit()

s = sane.open(available[0][0])
s.mode = 'color'

def do_scan(output_filename):
    # s.br_x=320. ; s.br_y=240.
    print 'Scanning with parameters:', s.get_parameters()

    s.start()
    print 'started'

    im = s.snap()
    print 'snapped'

    im.save(output_filename)

    # s.close()
    # sane.exit()


class ScanWorker(threading.Thread):
    def __init__(self, output_filename):
        super(ScanWorker, self).__init__()
        self.output_filename = output_filename
    def run(self):
        do_scan(self.output_filename)


class ScanDialog(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.worker = None
        self.elapsed = 0
        self.initUI()

    def initUI(self):

        self.parent.title("Scan images")
        self.pack(fill=BOTH, expand=1)

        Label(self, text="Name prefix:").grid(row=0, column=0)
        Label(self, text="Number suffix:").grid(row=0, column=1)

        self.newName = StringVar()
        self.newName.set('Scan_')
        newName = Entry(self, textvariable=self.newName, width=60)
        newName.grid(row=1, column=0)
        newName.bind("<Return>", lambda event: self.scan())
        newName.bind("<Escape>", lambda event: self.parent.destroy())
        newName.focus_set()
        self.newNameEntry = newName

        self.numberSuffix = Spinbox(self, from_=1, to=999)
        self.numberSuffix.grid(row=1, column=1)

        self.okButton = Button(self, text="Scan", command=self.scan, width=60, height=5)
        self.okButton.grid(row=3, column=0)

        cancelButton = Button(self, text="Cancel", command=self.parent.destroy)
        cancelButton.grid(row=3, column=1)

        self.statusLabel = Label(self, text="Idle")
        self.statusLabel.grid(row=4, column=0, columnspan=2)

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
            self.statusLabel.config(text='Idle')

    def scan(self):
        target = '%s%03d.jpg' % (self.newName.get(), int(self.numberSuffix.get()), )
        if os.path.exists(target):
            print 'Not scanning: %s - file exists!' % target
            return
        print "Scanning to filename '%s' ..." % (target, )
        if self.worker is None:
            self.worker = ScanWorker(target)
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

