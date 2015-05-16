__author__ = 'ishan'

from gi.repository import Gtk, GtkSource, Gio, GLib
from . import footer, terminal
from .file import FileChooser
import core


class Tabs(footer.Footer, Gtk.Grid, core.Language):
    """
        handles the addition and deletion of tabs in the notebook
    """

    page_count = 0

    def __init__(self, window, type):
        """
        creates an entire function new-tab
        :param window: the Main Window in main.py
        :param type: action type (create)
        :return: Gtk.Grid that can be packed directly into a tab
        """
        fc = FileChooser(window, type)
        response = fc.run()

        if response == Gtk.ResponseType.OK:
            print("File Selected : %s" % fc.get_filename())
        self.filename = fc.get_filename()
        fc.close()
        footer.Footer.__init__(self)
        Gtk.Grid.__init__(self)
        core.Language.__init__(self)
        self.code = GtkSource.View()
        self.language = None
        self.terminal = terminal.Terminal()

        # add customization
        self.customize()
        Tabs.page_count += 1

        # pack everything into self (Gtk.Grid)
        self.get_packed()

    @staticmethod
    def set_expand(widget):
        widget.set_hexpand(True)
        widget.set_vexpand(True)

    @staticmethod
    def wrap_scrolled(widget):
        sw = Gtk.ScrolledWindow()
        sw.add(widget)
        return sw

    def customize(self):
        """
            replacing Gtk.TextBuffer with GtkSource.Buffer to avoid the error on self.buffer.set_language
            currently open bug at https://bugzilla.gnome.org/show_bug.cgi?id=643732
        """

        self.code.set_buffer(GtkSource.Buffer())

        # expanding widgets
        for widget in [self.code, self.terminal]:
            Tabs.set_expand(widget)
        self.code.set_auto_indent(True)
        self.code.set_highlight_current_line(True)
        self.code.set_indent_on_tab(True)
        self.code.set_indent_width(4)
        self.code.set_insert_spaces_instead_of_tabs(True)
        self.code.set_show_line_numbers(True)

    def get_packed(self):
        """
        this method packs all the widget a single tab has
        into self (this instance) i.e. the grid instance
        prototype -> attach(child, left, top, width, height)
        :return: None
        """

        self.set_column_spacing(5)

        # attach editor widget
        self.attach(Tabs.wrap_scrolled(self.code), 0, 0, 2, 2)

        # attach the virtual terminal widget
        self.attach(Tabs.wrap_scrolled(self.terminal), 0, 2, 2, 2)

        # attach combobox language selector
        self.attach(self.combobox, 1, 4, 1, 1)

        # attach combobox changing event
        self.combobox.connect('changed',
                              self.change_language_from_combobox, self.code)

        # setting row-spacing
        self.set_row_spacing(5)
        self.set_column_spacing(5)

        # load buffer and perform further stuff
        self.load_buffer()

    def load_buffer(self):
        # open file
        text = open(self.filename, 'r').read()
        buffer = self.code.get_buffer()
        buffer.insert_at_cursor(text, len(text))
        buffer.set_modified(True)

        # set current combobox language
        self.language = self.set_language_with_file(self.combobox, self.code, self.filename)


    def get_label_widget(self):
        """
        this method returns a widget to be used as a label for each tab
        it also contains a close button which is connected to a function
        in the Main class
        :return: Gtk.HBox: directly packable into tab-label after connecting
                            close button
        """
        box = Gtk.HBox()
        starting_index = self.filename[::-1].find('/')
        self.custom_name = self.filename[-starting_index:]
        label = Gtk.Label(self.custom_name)
        close_button = Gtk.Button()
        close_icon = Gtk.Image()
        # set icon type, size
        close_icon.set_from_stock('gtk-close', 2)
        close_button.set_image(close_icon)
        close_button.set_relief(Gtk.ReliefStyle.NONE)

        # pack everything into box
        box.pack_start(label, True, True, 0)
        box.pack_start(close_button, True, True, 0)

        return box
