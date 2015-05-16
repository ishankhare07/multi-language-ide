__author__ = 'ishan'

from gi.repository import Gtk

class FileChooser:
    def __init__(self, parent, action, title="File Chooser"):
        if action is "open":
            action = Gtk.FileChooserAction.OPEN
        elif action is "create":
            action = Gtk.FileChooserAction.SAVE
        elif action is "folder":
            action = Gtk.FileChooserAction.CREATE_FOLDER

        self.fc = Gtk.FileChooserDialog(title,
                                        parent,
                                        action,
                                        buttons=(Gtk.STOCK_CANCEL,
                                                 Gtk.ResponseType.CANCEL,
                                                 Gtk.STOCK_OPEN,
                                                 Gtk.ResponseType.OK))

    def run(self):
        return self.fc.run()

    def close(self):
        self.fc.destroy()

    def get_filename(self):
        return self.fc.get_filename()