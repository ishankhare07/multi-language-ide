__author__ = 'ishan'

from gi.repository import Gtk, Vte, GLib, Gdk
import os

class Terminal(Vte.Terminal):
    def __init__(self, cwd=''):
        Vte.Terminal.__init__(self)
        self.spawn_sync(
            Vte.PtyFlags.DEFAULT,               # flags from Vte.PtyFlags
            cwd,                                # set current working directory
            ['/bin/sh'],                        # child’s argument vector
            [],                                 # a list of environment variables to be added to the environment
                                                # before starting the process, or None
            GLib.SpawnFlags.DO_NOT_REAP_CHILD,  # flags from GLib.SpawnFlags
            None,                               # an extra child setup function to run in the child just before exec(),
                                                # or None
            None,                               # user data for child_setup
            None                                # a Gio.Cancellable, or None
        )

        # set a green font foreground color
        self.set_color_foreground(Gdk.RGBA(0, 1, 0, 1))