__author__ = 'ishan'

import gi
gi.require_version("Vte", "2.90")
from gi.repository import Gtk, Vte, GLib, Gdk
import os

class Terminal(Vte.Terminal):
    def __init__(self):
        Vte.Terminal.__init__(self)
        self.fork_command_full(
            Vte.PtyFlags.DEFAULT,
            os.environ['HOME'],
            ['/bin/sh'],
            [],
            GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None,
            None
        )

        # set a green font foreground color
        self.set_color_foreground(Gdk.RGBA(0, 1, 0, 1).to_color())