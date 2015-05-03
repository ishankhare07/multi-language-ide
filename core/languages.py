from gi.repository import Gtk, GtkSource, GObject

GObject.type_register(GtkSource.View)


class Language:
    compilers = {
        'c': ['gcc', '.c'],
        'cpp': ['g++', '.cpp'],
        'java': ['javac', '.java']
    }

    interpreters = {
        'python': ['python', '.py'],
        'python3': ['python3', '.py'],
        'ruby': ['ruby', '.rb'],
        'perl': ['perl', '.pl']
    }

    def __init__(self):
        self.lm = GtkSource.LanguageManager()

    def change_language(self, name, sourceview):
        sourceview.get_buffer().set_language(self.lm.get_language(name))