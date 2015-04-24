from gi.repository import Gtk
import dir_core

class Tree:
    def __init__(self):
        self.dir_tree = dir_core.Directory().childs
        self.treestore = Gtk.TreeStore(str)

    def parse_tree(self):
        
