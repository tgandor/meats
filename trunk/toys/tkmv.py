#!/usr/bin/env python

import sys
import os

if len(sys.argv) < 2:
    print 'Usage: %s <filename>' % sys.argv[0]
    # exit()

from Tkinter import Frame, Tk, Button, BOTH, Label, Entry, StringVar, END

class RenameDialog(Frame):
    def __init__(self, parent, filename):
        Frame.__init__(self, parent)
        self.parent = parent
        self.filename = filename
        self.initUI()

    def initUI(self):

        self.parent.title("Rename file")
        self.pack(fill=BOTH, expand=1)

        originLabel = Label(self, text="File: " + self.filename)
        originLabel.grid(row=0, column=0, columnspan=2)

        renameLabel = Label(self, text="Rename to:")
        renameLabel.grid(row=1, column=0, columnspan=2)

        self.newName = StringVar()
        self.newName.set(self.filename)
        newName = Entry(self, textvariable=self.newName, width=80)
        endpos = self.filename.rfind('.')
        newName.selection_range(0, endpos if endpos > 0 else END)
        newName.grid(row=2, column=0, columnspan=2)
        newName.bind("<Return>", lambda event: self.doRename())
        newName.bind("<Escape>", lambda event: self.parent.destroy())
        newName.focus_set()

        okButton = Button(self, text="OK", command=self.doRename)
        okButton.grid(row=3, column=0)

        cancelButton = Button(self, text="Cancel", command=self.parent.destroy)
        cancelButton.grid(row=3, column=1)


    def doRename(self):
        print "Should rename '%s' to '%s'..." % (self.filename, self.newName.get())
        os.rename(self.filename, self.newName.get())
        self.parent.destroy()


root = Tk()
ex = RenameDialog(root, sys.argv[1])
root.geometry("650x100+300+300")
root.mainloop()
