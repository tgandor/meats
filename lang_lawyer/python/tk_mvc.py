#!/usr/bin/env python

# A demo from:
# https://stackoverflow.com/questions/46948606/mvc-tkinter-model-switch-between-frames-add-new-one-on-the-run
# this example has some strange stuff (e.g. you can try to switch to a page, before it is even created),
# and finally lacks a 'consolidated text' version (answers only tell what to fix).

# It's not as much a demo of MVC, but of a tkinter application having many navigable screens
# (a finite state machine)

try:
    import tkinter as tk                # python 3
    from tkinter import font as tkfont # python 3
except ImportError:
    import Tkinter as tk     # python 2
    import tkFont as tkfont  # python 2


# Controller


class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.container = container  # HERE: this is the parent for pages

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        print('Showing frame:', frame)
        frame.tkraise()

    def add_new(self):
        ''' Create a new frame on the run '''
        # HERE: the PageNew needs to get container as parent, not tk.Frame(self)
        self.frames["PageNew"] = PageNew(parent=self.container, controller=self)
        self.frames["PageNew"].grid(row=0, column=0, sticky="nsew")


# Views


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the start page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Go to Page One", command=lambda: controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="Go to Page Two", command=lambda: controller.show_frame("PageTwo"))
        button3 = tk.Button(self, text="Go to New Page", command=lambda: controller.show_frame("PageNew"))
        button1.pack()
        button2.pack()
        button3.pack()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Create a new page, go to the start page", command=self.on_click)
        button.pack()

    def on_click(self):
        self.controller.add_new()
        self.controller.show_frame("StartPage")


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button1 = tk.Button(
            self, text="Go to the start page", command=lambda: controller.show_frame("StartPage"))
        button2 = tk.Button(self, text="Go to the new page",
                       command=lambda: controller.show_frame("PageNew"))
        button1.pack()
        button2.pack()


class PageNew(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the new page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(
            self, text="Go to the start page", command=lambda: controller.show_frame("StartPage")
        )
        button.pack()


# Contrary to the name, there is no Model in this example


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
