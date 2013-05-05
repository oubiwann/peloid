from twisted.python import log

from peloid import const


commandError = {"error": "Command not found."}
shellError = """
The command you entered did not make sense; please try again.

To see a list of available commands, please type 'help' or '?'
"""


class CommandParser(object):
    """
    """
    def __init__(self):
        self.command = None
        self.rest = None
        self.result = None

    def prepCommand(self, input):
        parts = input.lower().split()
        self.command = parts[0]
        self.rest = []
        if len(parts) > 1:
            self.rest = parts[1:]

    def parseCommand(self, input):
        self.prepCommand(input)
        if self.command in const.cmds.help:
            self.result = self.cmd_help(rest)
        else:
            self.result = commandError
        return self.result

    def isError(self):
        if not isinstance(self.result, dict):
            return False
        if self.result.get("error"):
            return True


class ShellCommandParser(CommandParser):
    """
    """
    def parseCommand(self, input):
        super(ShellCommandParser, self).parseCommand(input)
        if self.isError():
            return shellError
        else:
            return self.result


class ObservingCommandParser(CommandParser):
    """
    """
    def cmd_look(self, at=""):
        # XXX get room description
        # XXX do a lookup on all contents in the room:
        #   if the first word in "at" is in the contents,
        #       do a lookup on that item and get is desc
        return "You look around..."

    def parseCommand(self, input):
        super(ObservingCommandParser, self).parseCommand(input)
        if not self.isError():
            return self.result
        elif self.command in const.cmds.look:
            self.result = self.cmd_look(self.rest)
        else:
            self.result = commandError
        return self.result


class MovingCommandParser(ObservingCommandParser):
    """
    """
    def cmd_go(self, direction):
        pass

    def parseCommand(self, input):
        super(MovingCommandParser, self).parseCommand(input)
        if not self.isError():
            return self.result
        elif self.command in const.cmds.go:
            # move player to room at given location
            self.result = None
        else:
            self.result = commandError
        return self.result


class HallsCommandParser(MovingCommandParser):
    """
    """
    def parseCommand(self, input):
        super(HallsCommandParser, self).parseCommand(input)
        if not self.isError():
            return self.result
        #elif self.command in const.cmds
        else:
            return commandError


class CreatorsCommandParser(CommandParser):
    """
    """


class ControllersCommandParser(CommandParser):
    """
    """


class AvatarsCommandParser(CommandParser):
    """
    """


class WordCommandParser(CommandParser):
    """
    """


class ViewingCommandParser(CommandParser):
    """
    """


class BanalityCommandParser(CommandParser):
    """
    """