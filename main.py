from gi.repository import Gtk
from gui.bind import directory_tree, Tabs, footer
import core
import time
import threading


class Main(Gtk.Notebook, core.Language):
    def __init__(self, build):
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

        # disable save, run, terminal button (no tab opened yet)
        self.builder.get_object('save').set_sensitive(False)
        self.builder.get_object('run').set_sensitive(False)
        self.builder.get_object('terminal').set_sensitive(False)

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

        # set save, run, terminal button active if not
        save_button = self.builder.get_object('save')
        run_button = self.builder.get_object('run')
        terminal_button = self.builder.get_object('terminal')

        for button in [save_button, run_button, terminal_button]:
            button.set_sensitive(True)

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
        name = Gtk.Buildable.get_name(widget)
        if name == 'new':
            param = 'create'
        elif name == 'button_open':
            param = 'open'
        else:
            param = 'create'
        self.notebook.append_page(*self.create_tab(param))
        self.notebook.show_all()

    def on_save_button_clicked(self, widget):
        """
        this method saves the text in source view of the current active tab
        into a file referred by self.filename of the current active tab
        :param widget: Gtk.Widget or Gtk.Button
        :return: None
        """
        active_page = self.get_active_tab()
        active_page.save()

    def on_destroy(self, *args):
        Gtk.main_quit(*args)

    def get_active_tab(self):
        active_index = self.notebook.get_current_page()
        active_page = self.notebook.get_nth_page(active_index)
        return active_page

    def on_term_clicked(self, button):
        """
        toggles the revealer for terminal
        :param button: Gtk.Widget or Gtk.Button
        :return: none
        """
        active_tab = self.get_active_tab()
        active_tab.toggle_revealer()

    def on_run_clicked(self, button):
        """
        this handles the run function
        :param button: Gtk.Widget or Gtk.Button
        :return: None
        """
        active_tab = self.get_active_tab()
        active_tab.save()                       # enables auto-save before running
        active_tab.execute()

    def hide(self):
        paned = self.builder.get_object('paned1')
        pos = paned.get_position()
        if pos > 0:
            while pos >= 0:
                paned.set_position(pos)
                time.sleep(0.005)
                pos -= 1
        else:
            pos = 0
            while pos <= 200:
                paned.set_position(pos)
                time.sleep(.005)
                pos += 1

    def on_hide_clicked(self, button):
        t = threading.Thread(target=self.hide)
        t.start()

builder = Gtk.Builder()
builder.add_from_file('gui/main.glade')
builder.connect_signals(Main(builder))
window = builder.get_object('window1')

window.show_all()
Gtk.main()
