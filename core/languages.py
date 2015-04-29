from gi.repository import Gtk, GtkSource, GObject

GObject.type_register(GtkSource.View)

class Language(GtkSource.LanguageManager):
    compilers = {
        'c': ['gcc', '.c'],
        'cpp': ['g++', '.cpp'],
        'java': ['javac', '.java']
    }

    interpreters = {
        'python' : ['python','.py'],
        'python3' : ['python3', '.py'],
        'ruby' : ['ruby','.rb'],
        'perl' : ['perl','.pl']
    }

    def __init__(self, language):
        GtkSource.LanguageManager.__init__(self)
        self.language = language

    def change_lanugage(self, name):
        self.language = name
        self.buffer.set_language(self.get_language(name))