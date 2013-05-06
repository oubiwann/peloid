from twisted.python import log

from peloid import const


commandError = {"error": "Command not found."}
shellError = """
The command you entered did not make sense; please try again.

To see a list of available commands, please type 'help' or '?'
"""


class CommandParser(object):
    """
    CommandParser subclasses are instantiated by the game when the game mode is
    set. The game mode is determined by the app.shell.service.getGameShellFactory
    function.

    Any object that has access to the game instance has acces to the parser
    instance (e.g., via game.parser).

    The point of interaction between the command parsing classes and the players
    is the .parserCommand method. See its docstring for more details.
    """
    def __init__(self):
        self.command = None
        self.rest = None
        self.result = None

    def prepCommand(self, input=""):
        parts = input.lower().split()
        self.command = []
        self.rest = []
        if parts:
            self.command = parts[0]
            if len(parts) > 1:
                self.rest = parts[1:]

    def parseCommand(self, input):
        """
        The user interacts with the MUD, regardless of shell/game/metagame, via
        commands typed in the MUD. Similarly, the only way for the MUD to relate
        to the player is by the results it sends back after parsing commands
        from the player.

        As such: anything that needs to be updated or presented to the user
        needs to be sent as part of the results that the user gets from the
        parseCommand call.

        If the game changes state in anyway that the user needs to be presented
        with such state info, the parseCommand results are where that info needs
        to be shared. Therefore, part of the parseCommand functionality needs to
        be the querying of a queue for user messages and the presnetation of
        those messages.
        """
        self.prepCommand(input)
        if self.command in const.cmds.help:
            self.result = self.cmd_help()
        elif self.command in const.cmds.emote:
            self.result = self.cmd_emote()
        else:
            self.result = commandError
        # XXX poll queue and get data to return to the user, if any
        # hopefully we can use a msg system that pushes, so we don't need to pull
        queueResults = ""
        result = self.result
        if not self.isError():
            result += queueResults
        return result

    def isError(self):
        if not isinstance(self.result, dict):
            return False
        if self.result.get("error"):
            return True

    def getNewline(self, count=1):
        return "\n:" * count

    def getHelp(self):
        return "%s This parser does not yet have 'help' information." % (
            self.getNewline())

    def cmd_help(self):
        if not self.rest:
            return self.getHelp()

    def cmd_emote(self):
        msg = "%s %s" % (self.game.player.name, " ".join(self.rest))
        # XXX send the message to the room queue that the player is in so that
        # all participants recieve it
        # XXX for now, do something silly, just return the message so that the
        # single user sees it
        return msg


class ShellCommandParser(CommandParser):
    """
    """
    def parseCommand(self, input):
        super(ShellCommandParser, self).parseCommand(input)
        if not self.isError():
            return self.result
        elif self.command in const.cmds.enter:
            self.result = self.cmd_enter()
            return self.result
        else:
            return shellError

    def cmd_enter(self):
        self.game.setMode(const.modes.lobby)
        # XXX the new mode corresponds to a new room being entered; the player
        # needs to be moved here, and upon entering, the room description
        # needs to be displayed


class ObservingCommandParser(CommandParser):
    """
    """
    def cmd_look(self):
        # XXX get room description
        # XXX do a lookup on all contents in the room:
        #   if the first word in "at" is in the contents,
        #       do a lookup on that item and get is desc
        if self.rest:
            return "You look at %s" % str(self.rest)
        return "You look around..."

    def parseCommand(self, input):
        super(ObservingCommandParser, self).parseCommand(input)
        if not self.isError():
            return self.result
        elif self.command in const.cmds.look:
            self.result = self.cmd_look()
        else:
            self.result = commandError
        return self.result


class MovingCommandParser(ObservingCommandParser):
    """
    """
    def cmd_go(self):
        if not self.rest:
            return "Where do you want to go?"
        return "You go %s ..." % self.rest

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


class WorldCommandParser(CommandParser):
    """
    """


class ViewingCommandParser(CommandParser):
    """
    """


class BanalityCommandParser(CommandParser):
    """
    """