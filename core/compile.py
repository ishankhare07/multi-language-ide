from .languages import Language
import os
import time


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
            CLikeFlow(compile_command, run_command, self.filename, terminal)

        elif language == "java":
            javaFlow(compile_command, run_command, self.filename, terminal)

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


class CLikeFlow:
    def __init__(self, compile_command, run_command, filename, terminal):
        """
        initializes the important attributes and calls the relevant functions
        itself. This should function out-of-the-box and the calling should code
        should not worry about calling the methods defined int this class to
        maintain the flow, the constructor should maintain this itself.
        :param compile_command: str, command to compile
        :param run_command: str, command to run
        :param filename: str, name of file to compile
        :param terminal: Vte.Terminal, terminal widget to execute command in
        :return: None
        """

        save_file_name = self.get_save_file_name(filename)
        self.remove_previous_output_file(save_file_name)
        self.full_compile_command = self.make_full_compile_command(compile_command,
                                                                   filename,
                                                                   save_file_name)
        # executing compile command
        self.do_compile(self.full_compile_command, terminal)

        if self.check_compile_success(save_file_name):         # proceed only if output file exists
            full_run_command = self.make_full_run_command(save_file_name)
            self.do_execute(full_run_command, terminal)

    def remove_previous_output_file(self, save_file_name):
        """
        it is necessary for detection of a failed compilation
        after a failed compilation there will be no output file to run
        which halts the reminal widget after the stderr
        :param save_file_name: str, name of output file
        :return: None
        """
        if os.path.exists(save_file_name):
            os.remove(save_file_name)

    def get_save_file_name(self, filename):
        """
        returns the filename to be used for the output file
        :param filename: str, name of file with extension
        :return: str, name of file without extension
        """
        index = filename.find('.')
        filename = filename[:index]

        return filename

    def make_full_compile_command(self, compile_command, filename, save_file_name):
        """
        generates the full compile command for a file
        output file name is given as filename without extension
        :param compile_command: str, command to run, eg gcc/g++ etc
        :param filename: str, name of file with extension
        :param save_file_name: str, name of file without extension
        :return: str, full compile command to feed into the terminal
        """

        command = ""
        command += compile_command + " -Wall "
        command += filename + " "               # name of file to compile
        command += "-o "                        # output option
        command += save_file_name               # name of output file
        command += "\n"                         # return key (enter)

        return command

    def make_full_run_command(self, save_file_name):
        """
        makes the full command for running an output file
        :param save_file_name: str, name of the output file
        :return: str, full run command to feed into the terminal
        """
        command = ""
        command += save_file_name
        command += "\n"

        return command

    def check_compile_success(self, save_file_name):
        """
        this method check for a successful compilation
        by checking the existence of the output file
        :param save_file_name: str, name of the output file
        :return: bool, True or False
        """
        time.sleep(1)
        if os.path.exists(save_file_name):
            print("compiled successfully", save_file_name, sep='\n')
            return True
        else:
            print("compilation not successful", save_file_name, sep='\n')
            return False

    def do_compile(self, full_compile_command, terminal):
        """
        This method handles the final feeding of the 'compile' command
        into the terminal widget. This is responsible for running the
        compile command on the provided filename
        :param full_compile_command: str, full command to compile the file
        :param terminal: Vte.Terminal, the terminal widget to execute the command in
        :return: None
        """
        length = len(full_compile_command)
        terminal.feed_child(full_compile_command, length)

    def do_execute(self, full_run_command, terminal):
        """
        This method handles the final feeding of the 'run' command
        into the terminal widget. This is responsible for executing
        the output file generated in the compile step
        :param full_run_command: str, full command to run
        :param terminal: Vte.Terminal, terminal widget to execute command into
        :return: None
        """

        length = len(full_run_command)
        terminal.feed_child(full_run_command, length)