#!/usr/bin/env python

import os
import threading

try:
    import Tkinter
except ImportError:
    os.system('sudo apt-get install python-tk')

from Tkinter import Frame, Tk, Button, BOTH, Label, Entry, StringVar, Spinbox, NORMAL, DISABLED
import tkMessageBox

try:
    import sane
except ImportError:
    os.system('sudo apt-get install sane sane-utils python-imaging-sane')

import sane
print 'SANE version:', sane.init()

available = sane.get_devices()
print 'Available devices =', available

if not available:
    print "NO DEVICES FOUND."
    exit()


class Settings(object):
    def __init__(self):
        self.width = 210.0
        self.height = 297.0


s = sane.open(available[0][0])
s.mode = 'color'
s.br_x = 210.0
s.br_y = 297.0

print 'Resolution: {0}'.format(s.resolution)
print 'Scanning with parameters:', s.get_parameters()


def do_scan(output_filename):
    s.start()
    print 'started'
    im = s.snap()
    print 'snapped'
    im.save(output_filename)
    return im


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
        self.extension = 'png'
        self.initUI()

    def initUI(self):

        self.parent.title("Scan Images")
        self.pack(fill=BOTH, expand=1)

        Label(self, text="Name prefix:").grid(row=0, column=0)
        Label(self, text="Number suffix:").grid(row=0, column=1)

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
        target = '%s%03d.%s' % (self.newName.get(), int(self.numberSuffix.get()), self.extension, )
        if os.path.exists(target):
            if not tkMessageBox.askokcancel(title='Scan Images', message='File exists. Overwrite?'):
                print 'Not scanning: %s - file exists!' % target
                new_name = self.newName.get()
                for i in xrange(int(self.numberSuffix.get()), 1000):
                    new_target = '%s%03d.%s' % (new_name, int(self.numberSuffix.get()), self.extension, )
                    if not os.path.exists(new_target):
                        print 'Next available filename: %s' % (new_target, )
                        self.numberSuffix.delete(0, 'end')
                        self.numberSuffix.insert(0, i)
                        break
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

