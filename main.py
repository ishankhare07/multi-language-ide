from gi.repository import Gtk, GtkSource, GObject
import core
from gui.bind import directory_tree, footer

GObject.type_register(GtkSource.View)


class Tabs(footer.Footer, Gtk.Grid):
    """
        handles the addition and deletion of tabs in the notebook
    """

    page_count = 0

    def __init__(self):
        """
            some stuff
        :return: Gtk.Grid that can be packed directly into a tab
        """
        footer.Footer.__init__(self)
        Gtk.Grid.__init__(self)
        self.code = GtkSource.View()
        self.code.language = 'c'
        self.input = Gtk.TextView()
        self.output = Gtk.TextView()

        # replace GtkSource buffer
        # and add customization
        self.custom_buffer()
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

    def custom_buffer(self):
        """
            replacing Gtk.TextBuffer with GtkSource.Buffer to avoid the error on self.buffer.set_language
            currently open bug at https://bugzilla.gnome.org/show_bug.cgi?id=643732
        """
        self.code.set_buffer(GtkSource.Buffer())

        # expanding widgets
        for widget in [self.code, self.input, self.output]:
            Tabs.set_expand(widget)
        self.code.set_auto_indent(True)
        self.code.set_highlight_current_line(True)
        self.code.set_indent_on_tab(True)
        self.code.set_indent_width(4)
        self.code.set_insert_spaces_instead_of_tabs(True)
        self.code.set_show_line_numbers(True)

        # non-editable output
        self.output.set_editable(False)

    def get_packed(self):
        """
        this method packs all the widget a single tab has
        into self (this instance) i.e. the grid instance
        :return: None
        """
        self.set_column_spacing(5)

        # attach editor widget
        self.attach(Tabs.wrap_scrolled(self.code), 0, 0, 2, 2)

        # set 'input' and 'output' labels
        self.attach(Gtk.Label('Input'), 0, 2, 1, 1)
        self.attach(Gtk.Label('Output'), 1, 2, 1, 1)

        # attach input and output textviews
        self.attach(Tabs.wrap_scrolled(self.input), 0, 3, 1, 2)
        self.attach(Tabs.wrap_scrolled(self.output), 1, 3, 1, 2)

        # attach combobox language selector
        self.attach(self.combobox, 1, 5, 1, 1)

        # attach combobox changing event
        self.combobox.connect('changed',
                              core.Language().change_language, self.code)

    def get_label_widget(self):
        """
        this method returns a widget to be used as a label for each tab
        it also contains a close button which is connected to a function
        in the Main class
        :return: Gtk.HBox: directly packable into tab-label after connecting
                            close button
        """
        box = Gtk.HBox()
        label = Gtk.Label("Page" + str(Tabs.page_count))
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


class Main(core.Compile, Gtk.Notebook, core.Language):
    def __init__(self, build):
        core.Compile.__init__(self)
        core.Language.__init__(self)
        Gtk.Notebook.__init__(self)
        self.notebook = Gtk.Notebook()
        self.footer = footer.Footer()
        self.builder = build
        self.filename = ""

        # add notebook to window()
        self.builder.get_object('notebook_holder').pack_end(self.notebook, True, True, 0)

        # add first tab
        self.notebook.append_page(*self.create_tab())

        # initialize the directory tree on cwd
        file_container = self.builder.get_object('files')
        dir_tree = directory_tree.Tree()
        treeview = dir_tree.create_tree_view()
        file_container.pack_start(treeview, True, True, 0)

    def create_tab(self):
        """
        this method is called by self.new_tab, which triggers on-click on new button
        creates a new tab
        get grid (Tabs()) from Tabs class
        fetches a label widget from Tabs.get_label_widget
        connects the close button in every tab
        :return: grid to be packed in tab body and label_widget to be set as tab title
        """
        tab = Tabs()
        label_widget = tab.get_label_widget()

        # connect label_widget's close button to close_tab()
        label_widget.get_children()[-1].connect('clicked', self.close_tab)
        label_widget.show_all()

        return tab, label_widget

    def close_tab(self, widget):
        """
        this method listens to the close button of each tab in the notebook
        :param widget: Gtk.Widget
        :return: None
        """
        page_num = self.notebook.get_current_page()
        self.notebook.remove_page(page_num)

    def new_tab(self, widget):
        """
        this method is called by the "new button" as specified in the glade xml file
        :param widget: Gtk.Widget or Gtk.Button
        :return: None
        """
        print('new tab added')
        self.notebook.append_page(*self.create_tab())
        self.notebook.show_all()

    def on_destroy(self, *args):
        Gtk.main_quit(*args)


builder = Gtk.Builder()
builder.add_from_file('gui/main.glade')
builder.connect_signals(Main(builder))
window = builder.get_object('window1')

window.show_all()
Gtk.main()
