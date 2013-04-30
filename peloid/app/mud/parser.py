from twisted.python import log

from peloid import const


class CommandParser(object):
    """
    """
    def prepCommand(self, input):
        parts = input.lower().split()
        command = parts[0]
        rest = []
        if len(parts) > 1:
            rest = parts[1:]
        return (command, rest)

    def parseCommand(self, input):
        command, rest = self.prepCommand(input)
        if command in const.cmds.look:
            return self.cmd_look(rest)
        elif command in const.cmds.go:
            # move player to room at given location
            pass
        else:
            return {"error": "Command not found."}

    def cmd_go(self, direction):
        pass

    def cmd_look(self, at=""):
        # XXX get room description
        # XXX do a lookup on all contents in the room:
        #   if the first word in "at" is in the contents,
        #       do a lookup on that item and get is desc
        return "You look around..."


class HallsCommandParser(CommandParser):
    """
    """
    def parseCommand(self, input):
        result = super(HallsCommandParser, self).parseCommand(input)
        if result:
            return result
        command, rest = self.prepCommand(input)


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