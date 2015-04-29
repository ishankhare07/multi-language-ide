from gi.repository import Gtk, GtkSource, GObject
import core
from gui.bind import directory_tree

GObject.type_register(GtkSource.View)

class Main(core.Compile, core.Language):
    def __init__(self, builder):
        core.Compile.__init__(self)
        core.Language.__init__(self,'c')
        self.builder = builder
        self.filename = ""
        """
            replacing Gtk.TextBuffer with GtkSource.Buffer to avoid the error on self.buffer.set_language
            currently open bug at https://bugzilla.gnome.org/show_bug.cgi?id=643732
        """
        self.builder.get_object('code').set_buffer(GtkSource.Buffer())
        self.buffer = self.builder.get_object('code').get_buffer()
        self.buffer.set_language(self.get_language('c'))

        #initialize the directory tree on cwd
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
