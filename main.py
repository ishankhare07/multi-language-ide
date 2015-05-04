from gi.repository import Gtk, GtkSource, GObject
import core
from gui.bind import directory_tree, header

GObject.type_register(GtkSource.View)


class Tabs:
    """
        handles the addition and deletion of tabs in the notebook
    """

    page_count = 0

    def __init__(self):
        """
            some stuff
        :return:
        """
        self.code = GtkSource.View()
        self.code.language = 'c'
        self.input = Gtk.TextView()
        self.output = Gtk.TextView()

        # replace GtkSource buffer
        # and add customization
        self.custom_buffer()
        Tabs.page_count += 1

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
        self.code.set_buffer(GtkSource.Buffer())

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

    def get_label_widget(self):
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

class TabStore:
    """
        stores the language information for each tab
    """
    def __init__(self):
        self.info = {}

    def add_info(self, tab_index, language_info):
        self.info[tab_index] = language_info

class Main(core.Compile, header.Header, Gtk.Notebook, core.Language):
    def __init__(self, builder):
        core.Compile.__init__(self)
        header.Header.__init__(self)
        core.Language.__init__(self)
        Gtk.Notebook.__init__(self)
        self.notebook = Gtk.Notebook()
        self.header = header.Header()
        self.store = TabStore()
        self.builder = builder
        self.filename = ""

        # attach language selector combobox
        self.builder.get_object('box3').pack_start(self.header.combobox, True, False, 0)
        self.header.combobox.connect('changed', self.trigger_language_update)

        # add notebook to window()
        self.builder.get_object('notebook_holder').pack_end(self.notebook, True, True, 0)

        # hear for page-switch
        self.notebook.connect('switch-page', self.page_changed)

        # add first tab
        self.notebook.append_page(*self.create_tab())

        # initialize the directory tree on cwd
        file_container = self.builder.get_object('files')
        dir_tree = directory_tree.Tree()
        treeview = dir_tree.create_tree_view()
        file_container.pack_start(treeview, True, True, 0)

    def page_changed(self, widget, page, page_num):
        # page_num1 = self.notebook.get_current_page()
        grid = self.notebook.get_nth_page(page_num)
        sourceview = grid.get_child_at(0, 0).get_child()
        lang = core.Language.get_language_index(sourceview.language)
        self.header.update_lang(lang)


    def create_tab(self):
        tab = Tabs()
        packed = tab.get_packed()
        label_widget = tab.get_label_widget()

        # connect label_widget's close button to close_tab()
        label_widget.get_children()[-1].connect('clicked', self.close_tab)
        label_widget.show_all()

        return packed, label_widget

    def close_tab(self, widget):
        page_num = self.notebook.get_current_page()
        self.notebook.remove_page(page_num)

    def trigger_language_update(self, combobox):
        index = combobox.get_active()
        model = combobox.get_model()
        lang = model[index][0]
        print("trigger =>", lang)

        page_num = self.notebook.get_current_page()
        grid = self.notebook.get_nth_page(page_num)
        # get scrolledwindow at 0,0 and then get sourceview from inside it
        sourceview = grid.get_child_at(0, 0).get_child()
        self.change_language(lang, sourceview)
        # self.store.add_info(page_num, lang)

    def new_tab(self, widget):
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
