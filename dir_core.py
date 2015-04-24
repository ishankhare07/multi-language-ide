import sys
import os

class Directory:
    def __init__(self, parent=None, indent=0):
        """
            directory to scan can be provided as a string
            example:
                Directory('/home/<user>/Desktop')
            or None to scan the current working directory
            example:
                Directory()
                is equivalent to:
                Directory(None)
            effect:
                creates a 'childs' attribute(self.childs), which can be accessed by
                dir = Directory()
                dir.childs
            childs:
                a nested dictionary containing the 
                    files -> with their name as keys and 'file' as value
                    directories -> as keys of nested dictionaries
        """

        self.childs = {}
        if parent == None:
            self.parent = os.getcwd()
        else:
            self.parent = parent
        self.indent = indent                        #for printing on the console
        self.dir_list = os.listdir(self.parent)

        for node in self.dir_list:
            if os.path.isfile(self.parent + '/' + node):
                print("\t" * self.indent + "file " + node)  #indent for printing on console, shows nested nature
                self.childs[node] = 'file'                  #adding the files under the current directory
            else:
                print("\t" * self.indent + "dir " + node)
                return_obj = Directory(parent=self.parent + '/' + node, indent=self.indent+1)   #save the new Directory object(depicts a nested directory)
                self.childs[node] = return_obj.childs       #add the nested dictionary to the parent dictionary
