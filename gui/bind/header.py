__author__ = 'ishan'

from gi.repository import Gtk, GtkSource

class Header:
    def __init__(self):
        """
            creates the combobox to be used in header
        """
        self.liststore = Gtk.ListStore(str)
        for lang in GtkSource.LanguageManager().get_language_ids():
            self.liststore.append([lang])
        self.combobox = Gtk.ComboBox()
        self.combobox.set_model(self.liststore)
        crt = Gtk.CellRendererText()
        self.combobox.pack_start(crt, True)
        self.combobox.add_attribute(crt, "text", 0)