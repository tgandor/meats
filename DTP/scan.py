#!/usr/bin/env python
from __future__ import print_function

import os
import sys
import time
import threading

try:
    if sys.version_info.major == 2:
        import Tkinter as tk
        import tkMessageBox
        import ttk
    else:
        import tkinter as tk
        from tkinter import messagebox as tkMessageBox
        from tkinter import ttk
except ImportError:
    tk, tkMessageBox = None, None
    os.system('sudo apt-get install python-tk')
    print('Please re-run to use Tkinter')
    exit()


try:
    import sane
except ImportError:
    sane = None
    print('Could not load sane')
    cmd = 'sudo apt-get install sane sane-utils python{}-sane'.format('3' if sys.version_info.major == 3 else '')
    print(cmd)
    os.system(cmd)
    print('Please re-run to use sane scanners')
    exit()


class Settings(object):
    def __init__(self, tk_root):
        self.resolution = tk.StringVar(tk_root, value='300')
        self.width = 210.0
        self.height = 297.0
        self.scale = tk.DoubleVar(tk_root, value=1.0)
        self.extension = tk.StringVar(tk_root, value='.png')
        self.scan_mode = tk.StringVar(tk_root, value='Color')
        self.custom_width = tk.StringVar(tk_root, value='210.0')
        self.custom_height = tk.StringVar(tk_root, value='297.0')

    def br_x(self):
        if self.scale.get() == 0:
            return float(self.custom_width.get())
        return self.width * self.scale.get()

    def br_y(self):
        if self.scale.get() == 0:
            return float(self.custom_height.get())
        return self.height * self.scale.get()

    def ext(self):
        return self.extension.get()

    def mode(self):
        return self.scan_mode.get()

    def configure_device(self, device):
        device.br_x = self.br_x()
        device.br_y = self.br_y()
        if self.mode() == 'gray+otsu':
            device.mode = 'Gray'
        else:
            if self.mode() in device['mode'].constraint:
                device.mode = self.mode()
            else:
                print("Mode '{}' not supported. Possible are: {}".format(self.mode(), device['mode'].constraint))
        device.resolution = int(self.resolution.get())

    def postprocess(self, image):
        if self.mode() == 'gray+otsu':
            try:
                import cv2
                import numpy
            except ImportError:
                print('Error - OpenCV (cv2) missing. Cannot postprocess.')
                return image
            else:
                cv_img = numpy.array(image)
                thresh, result = cv2.threshold(cv_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                print('Determined threshold: {0}'.format(thresh))
                return image.fromarray(result)
        else:
            return image


def do_scan(output_filename, settings):
    settings.configure_device(s)
    print('Resolution: {0}'.format(s.resolution))
    print('Scanning with parameters:', s.get_parameters())
    s.start()
    print('started')
    im = s.snap()
    print('snapped')
    im = settings.postprocess(im)
    print('postprocessed')
    im.save(output_filename)
    return im


class ScanWorker(threading.Thread):
    def __init__(self, output_filename, settings):
        super(ScanWorker, self).__init__()
        self.output_filename = output_filename
        self.settings = settings

    def run(self):
        do_scan(self.output_filename, self.settings)


class ScanDialog(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.worker = None
        self.elapsed = 0
        self.settings = Settings(self)

        # self.initUI() follows

        self.parent.title("Scan Images")
        self.pack(fill=tk.BOTH, expand=1)

        r = 0  # current grid row

        tk.Label(self, text="Name prefix:").grid(row=r, column=0)
        tk.Label(self, text="Number suffix:").grid(row=r, column=1)
        r += 1

        self.newName = tk.StringVar()
        self.newName.set(time.strftime('%Y%m%d_'))
        new_name = tk.Entry(self, textvariable=self.newName, width=60)
        new_name.grid(row=1, column=0)
        new_name.bind("<Return>", lambda event: self.scan())
        new_name.bind("<KP_Enter>", lambda event: self.scan())
        new_name.bind("<Escape>", lambda event: self.parent.destroy())
        new_name.select_from(0)
        n = len(self.newName.get()) - 1
        new_name.select_to(n)
        new_name.icursor(n)
        new_name.focus_set()
        self.newNameEntry = new_name

        self.numberSuffix = tk.Spinbox(self, from_=1, to=999)
        self.numberSuffix.bind("<Return>", lambda event: self.scan())
        self.numberSuffix.bind("<KP_Enter>", lambda event: self.scan())
        self.numberSuffix.grid(row=r, column=1)
        r += 1

        self.okButton = tk.Button(self, text="Scan", command=self.scan, width=55, height=5)
        self.okButton.grid(row=r, column=0)

        tk.Button(self, text="Exit", command=self.parent.destroy, width=12, height=5).grid(row=r, column=1)
        r += 1

        settings_panel = tk.Frame(self)

        panel = tk.Frame(settings_panel)
        tk.Label(panel, text="Paper Format").pack()
        tk.Radiobutton(panel, text="A4", value=1.0, variable=self.settings.scale).pack(anchor=tk.W)
        tk.Radiobutton(panel, text="A5", value=2 ** (-0.5), variable=self.settings.scale).pack(anchor=tk.W)
        tk.Radiobutton(panel, text="A6", value=0.5, variable=self.settings.scale).pack(anchor=tk.W)
        tk.Radiobutton(panel, text="Custom (W x H) [mm]", value=0.0, variable=self.settings.scale).pack(anchor=tk.W)
        tk.Entry(panel, textvariable=self.settings.custom_width).pack(anchor=tk.W)
        tk.Entry(panel, textvariable=self.settings.custom_height).pack(anchor=tk.W)
        panel.pack(side=tk.LEFT, anchor=tk.N)

        panel = tk.Frame(settings_panel)
        tk.Label(panel, text="File Format").pack()
        tk.Radiobutton(panel, text="PNG", value='.png', variable=self.settings.extension).pack(anchor=tk.W)
        tk.Radiobutton(panel, text="JPG", value='.jpg', variable=self.settings.extension).pack(anchor=tk.W)
        panel.pack(side=tk.LEFT, anchor=tk.N)

        panel = tk.Frame(settings_panel)
        tk.Label(panel, text="Scan Mode").pack()
        tk.Radiobutton(panel, text="Color", value='Color', variable=self.settings.scan_mode).pack(anchor=tk.W)
        tk.Radiobutton(panel, text="Gray", value='Gray', variable=self.settings.scan_mode).pack(anchor=tk.W)
        tk.Radiobutton(panel, text="Lineart", value='Lineart', variable=self.settings.scan_mode).pack(anchor=tk.W)
        tk.Radiobutton(panel, text="Gray+Otsu", value='gray+otsu', variable=self.settings.scan_mode).pack(anchor=tk.W)
        panel.pack(side=tk.LEFT, anchor=tk.N)

        panel = tk.Frame(settings_panel)
        tk.Label(panel, text="DPI").pack()
        tk.Radiobutton(panel, text="300", value='300', variable=self.settings.resolution).pack(anchor=tk.W)
        tk.Radiobutton(panel, text="150", value='150', variable=self.settings.resolution).pack(anchor=tk.W)
        panel.pack(side=tk.LEFT, anchor=tk.N)

        settings_panel.grid(row=r, column=0, columnspan=2)
        r += 1

        self.statusLabel = tk.Label(self, text="Please wait, initializing sane...")
        self.statusLabel.grid(row=r, column=0, columnspan=2)

    def _check_alive(self):
        if self.worker is None:
            return
        if self.worker.is_alive():
            self.after(100, self._check_alive)
            self.elapsed += 1
            self.statusLabel.config(text='Scanning, please wait... (%.1f s)' % (self.elapsed/10.0))
        else:
            self.worker = None
            self.okButton.config(state=tk.NORMAL)
            self.numberSuffix.invoke('buttonup')
            self.newNameEntry.focus_set()
            self.statusLabel.config(text='Idle (last scan: %.1f s)' % (self.elapsed/10.0))

    def _ext(self):
        return self.settings.ext()

    def scan(self):
        target = '%s%03d%s' % (self.newName.get(), int(self.numberSuffix.get()), self._ext(), )
        if os.path.exists(target):
            if not tkMessageBox.askokcancel(title='Scan Images', message='File exists. Overwrite?'):
                print('Not scanning: %s - file exists!' % target)
                new_name = self.newName.get()
                for i in range(int(self.numberSuffix.get()), 1000):
                    new_target = '%s%03d.%s' % (new_name, int(self.numberSuffix.get()), self._ext(), )
                    if not os.path.exists(new_target):
                        print('Next available filename: %s' % (new_target, ))
                        self.numberSuffix.delete(0, 'end')
                        self.numberSuffix.insert(0, i)
                        break
                return

        print("Scanning to filename '%s' ..." % (target,))

        if s is None:
            print('No scanner present. Connect and restart application.')
            return

        if self.worker is None:
            self.worker = ScanWorker(target, self.settings)
            self.worker.start()
            self.elapsed = 0
            self.after(100, self._check_alive)
            self.okButton.config(state=tk.DISABLED)
            self.statusLabel.config(text='Scanning, please wait...')
        else:
            print("Error - not started, worker exists.")


class DeviceDialog(tk.Toplevel):
    def __init__(self, scan_dialog, available, start_time=None):
        self.scan_dialog = scan_dialog
        self.parent = scan_dialog.parent
        self.init_time = time.time()
        self.start_time = start_time or time.time()
        tk.Toplevel.__init__(self, self.parent)
        self.title('Scan Images - Device Selection')
        self.geometry('200x150')
        tk.Label(self, text='Choose device:').pack()
        self.chosen = tk.StringVar()
        self.devices_combo = ttk.Combobox(self, textvariable=self.chosen, values=available)
        self.devices_combo.insert(0, available[0])
        self.devices_combo.pack()
        tk.Button(self, text='OK', command=self.choose).pack()
        print('{} Device choice initialized'.format(time.time() - self.start_time))

    def choose(self):
        global s
        print('{} Choice made = {} (took {:.1f} s)'.format(
            time.time() - self.start_time,
            self.chosen.get(),
            time.time() - self.init_time
        ))
        start_open = time.time()
        s = sane.open(self.chosen.get())
        stop_open = time.time()
        print('{} Device opened. (took {:.1f} s)'.format(stop_open - self.start_time, stop_open - start_open))
        total = self.init_time - self.start_time + time.time() - start_open
        self.scan_dialog.statusLabel.config(text='Idle (sane loaded in {:.1f} s)'.format(total))
        self.destroy()


def _init_sane(dialog):
    global s
    s = None
    start = time.time()
    version = sane.init()
    print('{} SANE version: {}, scanning devices...'.format(time.time() - start, version))

    available = sane.get_devices()
    print('{} Available devices = {}'.format(time.time() - start, available))

    if not available:
        print("NO DEVICES FOUND.")
        s = None
        dialog.statusLabel.config(text='Idle (no sane devices found) {:.1f} s'.format(time.time() - start))
    else:
        if len(available) > 1:
            DeviceDialog(dialog, [row[0] for row in available], start_time=start)
            return

        print('{} Opening first device: {}'.format(time.time() - start, available[0]))
        open_start = time.time()
        s = sane.open(available[0][0])
        print('{} Device opened in {:.1f} s'.format(time.time() - start, time.time() - open_start))
        dialog.statusLabel.config(text='Idle (sane loaded in {:.1f} s)'.format(time.time() - start))


if __name__ == '__main__':
    root = tk.Tk()
    ex = ScanDialog(root)
    root.geometry("+300+300")
    root.after(1, lambda: threading.Thread(target=_init_sane, args=(ex,)).start())
    root.mainloop()
