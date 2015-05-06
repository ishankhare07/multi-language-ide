__author__ = 'ishan'

from gi.repository import Gtk, GtkSource

class Footer:
    def __init__(self):
        """
            creates the combobox to be used in footer
        """
        self.liststore = Gtk.ListStore(str)
        lang_ids = GtkSource.LanguageManager().get_language_ids()
        lang_ids.sort()
        for lang in lang_ids:
            self.liststore.append([lang])
        self.combobox = Gtk.ComboBox()
        self.combobox.set_model(self.liststore)
        crt = Gtk.CellRendererText()
        self.combobox.pack_start(crt, True)
        self.combobox.add_attribute(crt, "text", 0)

    def update_lang(self, language):
        print("language => ", language)
        self.combobox.set_active(language)