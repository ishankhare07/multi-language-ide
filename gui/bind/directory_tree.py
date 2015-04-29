from gi.repository import Gtk
from core import dir_core

class Tree:
    def __init__(self, directory=None):
        self.dir_tree = dir_core.Directory(directory).childs
        self.treestore = Gtk.TreeStore(str)
        self.parse_tree(self.dir_tree)

    def parse_tree(self, dir_tree, parent=None):
        """
            parses the nested dictionary and builds the treestore model
        """

        for key, value in dir_tree.items():
            if isinstance(value, dict):                         #is a directory
                print('found parent')
                parent = self.treestore.append(parent,[key])    #append directory to tree and store back treeiter
                self.parse_tree(value, parent)                  #hence recurese into that directory
            else:                                               #is a file
                print('found child')
                if parent == None:                              #file on root level
                    self.treestore.append(None, [key])          #append it as it is(on root level)
                else:
                    self.treestore.append(parent, [key])        #append as a child of parent(folder)

    def create_tree_view(self):
        """
            creates the treeview with model
            also creates the columns and cellrenderers
        """

        self.treeview = Gtk.TreeView(model=self.treestore)      #main textview
        tvc = Gtk.TreeViewColumn("file/directory names")        #specify textview columns
        self.treeview.append_column(tvc)                        #append it to treeview

        crt = Gtk.CellRendererText()                            #create text-cell-renderer for treeview
        tvc.pack_start(crt, True)                               #pack cell renderer into that particular treeviewcolumn
        tvc.add_attribute(crt, "text", 0)                        #get text attribute of 1st column(0th index) from the model

        return self.treeview
