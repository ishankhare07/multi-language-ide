import sys
import os

class Directory:
    def __init__(self, parent=None, indent=0):
        if parent == None:
            self.parent = os.getcwd()
        else:
            self.parent = parent
        self.indent = indent
        self.dir_list = os.listdir(self.parent)
        for node in self.dir_list:
            if os.path.isfile(self.parent + '/' + node):
                #print('path : ' + self.parent)
                print("\t" * self.indent + "file " + node)
            else:
                #print('path : ' + self.parent)
                print("\t" * self.indent + "dir " + node)
                #if not node == "__pycache__":
                Directory(parent=self.parent + '/' + node, indent=self.indent+1)
