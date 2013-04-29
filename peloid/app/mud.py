from twisted.python import log

from peloid import const


class World(object):
    """
    """


class Player(object):
    """
    """


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


class Game(object):
    """
    """
    def __init__(self):
        self.mode = None
        self.parser = None

    def start(self, *args, **kwargs):
        pass

    def setMode(self, mode):
        """
        Legal modes are:
         * const.modes.lobby
         * const.modes.create
         * const.modes.controll
         * const.modes.avatar
         * const.modes.play
         * const.modes.observe
         * const.modes.chat

        These correspond to the following in-game locations:
         * Hall of Halls
         * Hall of Creators
         * Hall of Contorllers
         * Hall of Avatars
         * anywhere in-game (in a World instance)
         * Hall of Viewing
         * Hall of Banality

        Each mode will have its own CommandParser.
        """
        self.mode = mode
        if self.mode == const.modes.lobby:
            self.parser = HallsCommandParser()
        elif self.mode == const.modes.create:
            self.parser = CreatorsCommandParser()
        elif self.mode == const.modes.controll:
            self.parser = ControllersCommandParser()
        elif self.mode == const.modes.avatar:
            self.parser = AvatarsCommandParser()
        elif self.mode == const.modes.play:
            self.parser = WordCommandParser()
        elif self.mode == const.modes.observe:
            self.parser = ViewingCommandParser()
        elif self.mode == const.modes.chat:
            self.parser = BanalityCommandParser()

    def parseCommand(self, input):
        return self.parser.parseCommand(input)