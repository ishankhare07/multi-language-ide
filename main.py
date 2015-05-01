from gi.repository import Gtk, GtkSource, GObject
import core
from gui.bind import directory_tree

GObject.type_register(GtkSource.View)

class Tabs(core.Language):
    """
        handles the addition and deletion of tabs in the notebook
    """

    def __init__(self):
        """
            some stuff
        :return:
        """
        core.Language.__init__(self, 'c')

        self.code = GtkSource.View()
        self.input = Gtk.TextView()
        self.output = Gtk.TextView()

        # replace GtkSource buffer
        # and add customization
        self.custom_buffer()

    def custom_buffer(self):
        """
            replacing Gtk.TextBuffer with GtkSource.Buffer to avoid the error on self.buffer.set_language
            currently open bug at https://bugzilla.gnome.org/show_bug.cgi?id=643732
        """
        self.code.set_buffer(GtkSource.Buffer)
        self.code.set_auto_indent(True)
        self.code.set_highlight_current_line(True)
        self.code.set_indent_on_tab(True)
        self.code.set_indent_width(4)
        self.code.set_insert_spaces_instead_of_tabs(True)
        self.code.set_show_line_numbers(True)


class Main(core.Compile, Gtk.Notebook):
    def __init__(self, builder):
        core.Compile.__init__(self)
        Gtk.Notebook.__init__(self)
        self.builder = builder
        self.filename = ""

        # initialize the directory tree on cwd
        file_container = self.builder.get_object('files')
        dir_tree = directory_tree.Tree()
        treeview = dir_tree.create_tree_view()
        file_container.pack_start(treeview, True, True, 0)

    def on_destroy(self, *args):
        Gtk.main_quit(*args)


builder = Gtk.Builder()
builder.add_from_file('gui/main.glade')
builder.connect_signals(Main(builder))
window = builder.get_object('window1')

window.show_all()
Gtk.main()
