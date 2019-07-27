"""
Shows that the tk widgets get updated when their variable (model)
is changed, without the need to access the widget in any way.
Their variables are not read-only.
"""

try:
    import tkinter as tk
except ImportError:
    try:
        import Tkinter as tk
    except ImportError:
        print('Missing tkinter - install python-tk or something.')
        exit()


def toggle(variable):
    if variable.get() == 'Hello':
        entry_var.set('world')
    else:
        entry_var.set('Hello')


root = tk.Tk()

entry_var = tk.StringVar(value='Hello')
dialog = tk.Frame(root)
entry = tk.Entry(dialog, textvariable=entry_var)
entry.pack(anchor=tk.N)
button = tk.Button(dialog, text='See rest', command=lambda: toggle(entry_var))
button.pack(anchor=tk.N)
dialog.pack()

root.mainloop()
