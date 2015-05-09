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

    def change_language(self, combobox, sourceview):
        """

        :param sourceview: GtkSource.View widget
        :param combobox: Gtk.Combobox widget
        :return: None
        """
        name = Language.get_language_name(combobox)
        sourceview.get_buffer().set_language(self.lm.get_language(name))
        # print("previous language =>", sourceview.language)
        sourceview.language = name
        # print("current language =>", sourceview.language)

    @staticmethod
    def get_language_name(combobox):
        """

        :param combobox: Gtk.Combobox
        :return: lang: (str) a language id to be fed into GtkSource.LanguageManager().get_language()
        """
        lm = GtkSource.LanguageManager().get_language_ids()
        lm.sort()

        index = combobox.get_active()
        lang = lm[index]

        return lang