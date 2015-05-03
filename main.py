from gi.repository import Gtk, GtkSource, GObject
import core
from gui.bind import directory_tree, header

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

    def set_expand(self, widget):
        widget.set_hexpand(True)
        widget.set_vexpand(True)

    def wrap_scrolled(self, widget):
        sw = Gtk.ScrolledWindow()
        sw.add(widget)
        return sw

    def custom_buffer(self):
        """
            replacing Gtk.TextBuffer with GtkSource.Buffer to avoid the error on self.buffer.set_language
            currently open bug at https://bugzilla.gnome.org/show_bug.cgi?id=643732
        """
        #self.code.set_buffer(GtkSource.Buffer)

        # expanding widgets
        for widget in [self.code, self.input, self.output]:
            self.set_expand(widget)
        self.code.set_auto_indent(True)
        self.code.set_highlight_current_line(True)
        self.code.set_indent_on_tab(True)
        self.code.set_indent_width(4)
        self.code.set_insert_spaces_instead_of_tabs(True)
        self.code.set_show_line_numbers(True)

        # non-editable output
        self.output.set_editable(False)

    def get_packed(self):
        grid = Gtk.Grid()
        grid.set_column_spacing(5)

        # attach editor widget
        grid.attach(self.wrap_scrolled(self.code), 0, 0, 2, 2)

        # set 'input' and 'output' labels
        grid.attach(Gtk.Label('Input'), 0, 2, 1, 1)
        grid.attach(Gtk.Label('Output'), 1, 2, 1, 1)

        # attach input and output textviews
        grid.attach(self.wrap_scrolled(self.input), 0, 3, 1, 2)
        grid.attach(self.wrap_scrolled(self.output), 1, 3, 1, 2)
        return grid


class Main(core.Compile):
    def __init__(self, builder):
        core.Compile.__init__(self)
        self.notebook = Gtk.Notebook()
        self.builder = builder
        self.filename = ""

        # attach language selector combobox
        self.builder.get_object('box3').pack_start(header.Header().widget, True, True, 0)

        # add notebook to window()
        self.builder.get_object('notebook_holder').pack_end(self.notebook, True, True, 0)

        # add first tab
        self.notebook.append_page(Tabs().get_packed(), None)

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
