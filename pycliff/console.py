#!/usr/bin/python3
import shlex
from typing import List
from .bindings import Bindings, CommandBindingException


class Console(object):
    """ Top level console object. This object sets up the console
        and loops to take user inputs as commands and execute them.
    """

    def __init__(self, prompt='>', greeting=''):
        """Args:
                prompt: str
                    Characters or a string to display at the beginning of
                    each input line. The default is '>'
                greeting: str
                    The message to display at the console's startup
        """
        self._running = False
        self._bindings = Bindings()
        self._objects = {}
        self.setPrompt(prompt)
        self.setGreeting(greeting)

    @property
    def argc(self):
        return self._bindings.argc

    def getArg(self, index, default=None):
        return self._bindings.getArg(index, default)

    def setPrompt(self, prompt: str) -> None:
        """ Set a new prompt for this console.
            Args:
                prompt: str
                    The new prompt
        """
        self._prompt = '\n{0} '.format(prompt)

    def setGreeting(self, greeting: str) -> None:
        """ Set a new greeting for this console.
            Args:
                greeting: str
                    The new message to display at the console's startup
        """
        self._greeting = greeting

    def useGreeting(self, filename: str) -> None:
        """ Instruct the console to use a greeting stored in a text file
            Args:
                filename: str
                    Path to the text file containing the greeting
        """
        with open(filename, 'r') as gfile:
            greeting = gfile.read()
            self._greeting = greeting

    def commandList(self) -> List[str]:
        """ Returns a list of all commands bound to this console
            Returns:
                commands: List[str]
                    A list of command strings bound to this console
        """
        return self._bindings.asList()

    def display(self, *messages: str) -> None:
        """ Display multiple lines of messages to the console
            Args:
                messages: str
                    Messages to display to the console
        """
        for message in messages:
            print(message)

    def register(self, command: str) -> callable:
        """ A decorator to bind a command handler to this console instance
            Args:
                command: str
                    Command string to invoke the decorated command handler
        """
        def decorator(handler: callable):
            return self._bindings.add(command, handler)
        return decorator

    def default(self, handler: callable) -> callable:
        """ A decorator to bind a default handler to this console instance
            Args:
                handler: function
                    A default handler function. Usually this is a function
                    to display help messages.
        """
        return self._bindings.setDefault(handler)

    def run(self) -> None:
        """ Launch the console in the interactive mode.
            This will loop indefinitely until the console
            is terminated with CTRL+C or otherwise.
        """
        if self._greeting:
            self.display(self._greeting)

        self._running = True
        try:
            while (self._running):
                response = input(self._prompt)
                self._process_command(response)
        except KeyboardInterrupt:
            self.display('', 'Exiting...')

    def execute(self, filename: str) -> None:
        """ Executes a script file instead of launching the console
            interactively. The script execution can be terminated
            early with CTRL+C.

            Args:
                filename: str
                    Path to the script file to execute
        """
        if self._greeting:
            self.display(self._greeting)

        try:
            with open(filename, 'r') as script:
                for command in script:
                    self._process_command(command)
        except (IOError, OSError) as e:
            self.display('An error occurred while opening script file')
        except KeyboardInterrupt:
            self.display('Terminating...')

    def stop(self) -> None:
        """ Stop the interactive mode of the console. This
            will cause the console to quit.
        """
        self._running = False

    def attach(self, key: str, obj: object) -> None:
        """ Attach an object to the console. Objects attached
            to the console are accessible by command handlers
            through the getObject() method.

            Args:
                key: str
                    A string to identify the object when
                    getObject gets called
                obj: object
                    The object to attach
        """
        self._objects[key] = obj

    def getObject(self, key: str, default=None) -> object:
        """ Returns an attached object identified by the key.
            If no such key is found, the default is returned.

            Args:
                key: str
                    A string to identify the object to retrieve
                default: object
                    Value to return when the key is not found
        """
        return self._objects.get(key, default)

    def _process_command(self, command: str) -> None:
        """ Internal helper method to parse and execute a command string.
        """
        command = shlex.split(command)
        try:
            self._bindings.execute(*command)
        except CommandBindingException as e:
            self.display(e)
