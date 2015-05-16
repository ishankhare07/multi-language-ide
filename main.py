from gi.repository import Gtk
import core
from gui.bind import directory_tree, Tabs, footer


class FileChooser:
    def __init__(self, parent, action, title='Choose a File'):
        if action is "choose":
            action = Gtk.FileChooserAction.OPEN
        elif action is "create":
            action = Gtk.FileChooserAction.SAVE
        elif action is "folder":
            action = Gtk.FileChooserAction.CREATE_FOLDER
        self.fc = Gtk.FileChooserDialog(title,
                                        parent,
                                        action,
                                        buttons=(
                                            Gtk.STOCK_CANCEL,
                                            Gtk.ResponseType.CANCEL,
                                            Gtk.STOCK_OPEN,
                                            Gtk.ResponseType.OK))
        self.fc.set_transient_for(parent)

    def on_close(self,):
        print('closing')
        self.fc.destroy()

    def run(self):
        response = self.fc.run()
        return response

    def get_filename(self):
        return self.fc.get_filename()


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
        # self.notebook.append_page(*self.create_tab())

        # initialize the directory tree on cwd
        file_container = self.builder.get_object('files')
        dir_tree = directory_tree.Tree()
        treeview = dir_tree.create_tree_view()
        file_container.pack_start(Tabs.wrap_scrolled(treeview), True, True, 0)

    def create_tab(self, type):
        """
        this method is called by self.new_tab, which triggers on-click on new button
        creates a new tab
        get grid (Tabs()) from Tabs class
        fetches a label widget from Tabs.get_label_widget
        connects the close button in every tab
        :param type: type of action to choose for filechooser dialog
        :return: grid to be packed in tab body and label_widget to be set as tab title
        """
        tab = Tabs(self.builder.get_object('window1'), type)
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
        self.notebook.append_page(*self.create_tab('create'))
        self.notebook.show_all()

    def on_destroy(self, *args):
        Gtk.main_quit(*args)


builder = Gtk.Builder()
builder.add_from_file('gui/main.glade')
builder.connect_signals(Main(builder))
window = builder.get_object('window1')

window.show_all()
Gtk.main()
