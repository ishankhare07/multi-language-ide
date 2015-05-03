__author__ = 'ishan'

from gi.repository import Gtk, GtkSource

class Header:
    def __init__(self):
        self.liststore = Gtk.ListStore(str)
        for lang in GtkSource.LanguageManager().get_language_ids():
            self.liststore.append([lang])
        self.widget = Gtk.ComboBox(model=self.liststore)
        crt = Gtk.CellRendererText()
        self.widget.pack_start(crt, True)
        self.widget.add_attribute(crt, "text", 0)

        self.widget.connect('changed', self.language_changed)

    def language_changed(self, widget):
        index = widget.get_active()
        model = widget.get_model()
        lang = model[index][0]
        print(lang)