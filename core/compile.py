from .languages import Language


class Compile:
    """
    This class works as a wrapper class for receiving the run events
    for different languages. The main job of this class is to factor out
    the common patterns in various language compilation flow and called
    the relevant class
    """
    def __init__(self, language, filename, terminal):
        """
        intializes the right commands and the right class
        instances for the correct language flow
        :param language: name of the language
        :param filename: name of the file
        :param terminal: the current active terminal instance
        :return: self
        """
        self.filename = filename
        self.terminal = terminal
        if language in Language.compilers.keys():
            compile_command = Language.compilers[language][0]
            run_command = Language.compilers[language][1]
            self.handle_compiled(language, compile_command, run_command, terminal)
        elif language in Language.interpreters.keys():
            run_command = Language.interpreters[language][0]
            self.handle_interpreted(run_command, terminal)

        else:
            print('language definition not supported')

    def handle_compiled(self, language, compile_command, run_command, terminal):
        """
        handles the compiled language compilation and execution by
        sorting out different language flow mechanisms and calling
        the right class
        :param language: str, name of the language
        :param compile_command: str, command to compile the source file
        :param run_command: str, command to run the compiled file
        :param terminal: Vte.Terminal, terminal widget to execute commands on
        :return: None
        """
        if language == "c" or language == "cpp":
            cLikeFlow(language, compile_command, run_command, self.filename, terminal)

        elif language == "java":
            javaFlow(language, compile_command, run_command, self.filename, terminal)

    def handle_interpreted(self, run_command, terminal):
        """
        handles the interpreted languages flow
        :param run_command: str, command to run the compiled file
        :param terminal: Vte.Terminal, terminal widget to execute command on
        :return: None
        """
        InterpretedFlow(run_command, self.filename, terminal)


class InterpretedFlow:
    """
    This class is called by the compiled class for executing and running
    a flow for interpreted languages like Python, Python3, Ruby, Perl.
    This class should manage the entire process from compilation to running
    in the terminal widget passed in.
    """
    def __init__(self, run_command, filename, terminal):
        """
        initializes the important attributes and calls the relevant functions
        itself. This should function out-of-the-box and the calling should code
        should not worry about calling the methods defined int this class to
        maintain the flow, the constructor should maintain this itself.
        :param run_command: str, command to run
        :param filename: str, name of file to run
        :param terminal: Vte.Terminal, terminal widget to run the programs in
        :return: None
        """
        self.run_command = run_command
        self.terminal = terminal

        full_command = self.make_full_command(run_command, filename)
        self.run(full_command, self.terminal)

    def make_full_command(self, run_command, filename):
        """
        build the final executing string to feed into the terminal
        :param run_command: command for running
        :param filename: name of file to execute
        :return: str, full command to be fed into the terminal widget
        """
        command = ''
        command += run_command + ' '
        command += filename
        command += '\n'

        return command

    def run(self, full_command, terminal):
        """
        final feeding of the command into the terminal widget
        :param full_command: full command string to feed into terminal
        :return: None
        """
        length = len(full_command)
        terminal.feed_child(full_command, length)