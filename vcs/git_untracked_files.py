#!/usr/bin/env python

# Based on: https://github.com/peterbrittain/asciimatics/blob/master/samples/contact_list.py

import os
import sys

from asciimatics.widgets import Frame, ListBox, Layout, Divider, Button, Widget
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication


class FileModel:
    def __init__(self):
        self.last_untracked = []

    def get_summary(self):
        files = os.popen("git status --porcelain").read().split("\n")
        self.last_untracked = [f[3:] for f in files if f.startswith("?? ")]
        return [(f, f) for f in self.last_untracked]

    def delete(self, filename):
        if filename is None:
            raise StopApplication("All deleted.")

        os.unlink(filename)

        n = len(self.last_untracked)
        if n > 1 and filename in self.last_untracked:
            idx = self.last_untracked.index(filename)
            return (
                self.last_untracked[idx + 1]
                if idx < n - 1
                else self.last_untracked[idx - 1]
            )

        return None


class ListView(Frame):
    def __init__(self, screen, model):
        super(ListView, self).__init__(
            screen,
            screen.height * 2 // 3,
            screen.width * 2 // 3,
            on_load=self._reload_list,
            hover_focus=True,
            can_scroll=False,
            title="Untracked files",
        )
        self._model = model

        # Create the form for displaying the files.
        self._list_view = ListBox(
            Widget.FILL_FRAME,
            model.get_summary(),
            name="untracked_files",
            add_scroll_bar=True,
            on_select=self._delete_one,
        )
        self._delete_button = Button("Delete All", self._delete)

        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._list_view)
        layout.add_widget(Divider())
        layout2 = Layout([1, 1])
        self.add_layout(layout2)
        layout2.add_widget(self._delete_button, 0)
        layout2.add_widget(Button("Quit", self._quit), 1)
        self._delete_button.disabled = True  # Not implemented
        self.fix()

    def _reload_list(self, new_value=None):
        self._list_view.options = self._model.get_summary()
        self._list_view.value = new_value

    def _delete(self):
        raise StopApplication("All deleted")

    def _delete_one(self):
        self.save()
        next_value = self._model.delete(self._list_view.value)
        if next_value is None:
            raise StopApplication("All deleted")
        self._reload_list(next_value)

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")


def main(screen, scene):
    scenes = [
        Scene([ListView(screen, contacts)], -1, name="Main"),
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)


contacts = FileModel()
last_scene = None
while True:
    try:
        Screen.wrapper(main, catch_interrupt=True, arguments=[last_scene])
        print("Done.")
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene
