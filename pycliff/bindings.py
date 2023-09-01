#!/usr/bin/python


class CommandBindingException(Exception):
    pass


class Bindings(object):
    """ This class maps commands (str) to handlers (functions)
        (i.e. binds the command to the handler). A handler
        can be bound to multiple commands, but each command can
        only be bound to a single handler.
    """

    def __init__(self):
        self._commands = {}
        self._default = None
        self._args = []

    def __contains__(self, key: str) -> bool:
        """ Enable the 'in' keyword to be used with a Binding object.

            Args:
                key: str
                    The command to test whether or not it's registered
                    to this binding.
            Returns:
                bool:
                    True if the command is registered, False otherwise
        """
        return key in self._commands

    @property
    def argc(self):
        return len(self._args)

    def getArg(self, index, default=''):
        if (index >= self.argc):
            return default
        return self._args[index]

    def add(self, command: str, handler: callable) -> callable:
        """ Add a handler and its associated command to this binding.

            Args:
                command: str
                    The command that will be used to invoke the handler
                handler:
                    Any function to be invoked when the given command
                    is executed

            Returns:
                handler: callable
                    This is the handler provided in the function params
        """
        self._commands[command] = handler
        return handler

    def setDefault(self, handler: callable) -> callable:
        """ Set the default handler for this binding.
            (i.e. the handler to execute when there is
            no matching command)

            Returns:
                handler: callable
                    The default handler itself
        """
        self._default = handler
        return handler

    def register(self, command: str):
        """ A decorator function to register a command and a handler
            to this binding.

            Args:
                command: str
                    The command that will invoke the handler
        """
        def decorator(handler: callable):
            return self.add(command, handler)
        return decorator

    def asList(self) -> int:
        """ Returns a list of all commands registered to this binding.
            Returns:
                commands: str
                    A list of all commands registered to this binding.
        """
        return sorted(self._commands.keys())

    def execute(self, *commands: str):
        """ Executes a registered handler that matches the given command.
            If no matching command is found, the default handler will be
            executed instead if there is one.
`
            Args:
                commands: str
                    A list of commands to execute

            Raises:
                CommandBindingException:
                    When the handler is not a callable
        """
        if (len(commands) == 0):
            return
        command, self._args = commands[0], commands[1:]
        handler = self._commands.get(command, self._default)
        if not callable(handler):
            raise CommandBindingException(f'{command}: command not recognized')
        return handler(*self._args)
