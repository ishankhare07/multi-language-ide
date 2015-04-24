from gi.repository import Gtk
import dir_core

class Tree:
    def __init__(self, directory=None):
        self.dir_tree = dir_core.Directory(directory).childs
        self.treestore = Gtk.TreeStore(str)
        self.parse_tree(self.dir_tree)

    def parse_tree(self, dir_tree, parent=None):
        for key, value in dir_tree.items():
            if isinstance(value, dict):                         #is a directory
                parent = self.treestore.append(None,[key])      #append directory to tree and store back treeiter
                self.parse_tree(value, parent)                  #hence recurese into that directory
            else:                                               #is a file
                if parent == None:                              #file on root level
                    self.treestore.append(None, [key])          #append it as it is(on root level)
                else:
                    self.treestore.append(parent, [key])        #append as a child of parent(folder)
