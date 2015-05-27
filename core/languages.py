from gi.repository import Gtk, GtkSource, GObject

GObject.type_register(GtkSource.View)


class Language:
    compilers = {
        'c': ['gcc', './'],
        'cpp': ['g++', './'],
        'java': ['javac', 'java']
    }

    interpreters = {
        'python': ['python', '.py'],
        'python3': ['python3', '.py'],
        'ruby': ['ruby', '.rb'],
        'perl': ['perl', '.pl']
    }

    def __init__(self):
        self.lm = GtkSource.LanguageManager()

    def change_language_from_combobox(self, combobox, sourceview):
        """

        :param sourceview: GtkSource.View widget
        :param combobox: Gtk.Combobox widget
        :return: None
        """
        name = Language.get_language_name(combobox)
        sourceview.get_buffer().set_language(self.lm.get_language(name))
        # print("previous language =>", sourceview.language)
        self.language = name
        # print("current language =>", sourceview.language)

    def set_language_with_file(self, combobox, sourceview, filename):
        """
        this method is particularly used to set combobox when opening a file
        :param combobox: Gtk.Combobox language selector which is to be set
        :param sourceview: GtkSource.View on which the language is to be set
        :param language: Str, name of language
        :return: Str, name of language
        """
        language = self.lm.guess_language(filename, None)
        lm_list = self.lm.get_language_ids()
        lm_list.sort()

        # setting language in combobox
        if language:
            index = lm_list.index(language.get_id())
            combobox.set_active(index)

        # setting language in sourceview
        sourceview.get_buffer().set_language(language)

        if language is not None:
            return language.get_id()
        else:
            return None

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
