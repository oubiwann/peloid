from twisted.python import log

from peloid import const
from peloid.app.mud import parser, player, room, world


class Game(object):
    """
    Notes:
     * the game object is instantiated by app.shell.service.getGameShellFactory
     * app.shell.gameshell.TerminalRealm then sets the game attribute
     * the game instance isn't started until a Manhole object is instantiated
    """
    def __init__(self, gameFile=None, player=None):
        self.gameFile = gameFile
        # XXX also, load game here
        self.mode = None
        self.parser = None
        self.player = player

    def loadGame(self):
        """
        When the game is loaded, there will be a door/exit in the Hall of
        Avatars, allowing one to enter the game world.
        """
        pass

    def start(self, *args, **kwargs):
        if self.gameFile:
            self.loadGame()

    def setMode(self, mode):
        """
        The game mode is set by app.shell.service.getGameShellFactory.

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
        playerClass = player.MetaPlayer
        if self.mode == const.modes.shell:
            playerClass = player.ShellPlayer
            self.parser = parser.ShellCommandParser()
        if self.mode == const.modes.lobby:
            self.parser = parser.HallsCommandParser()
        elif self.mode == const.modes.create:
            self.parser = parser.CreatorsCommandParser()
        elif self.mode == const.modes.controll:
            self.parser = parser.ControllersCommandParser()
        elif self.mode == const.modes.avatar:
            self.parser = parser.AvatarsCommandParser()
        elif self.mode == const.modes.play:
            playerClass = player.GamePlayer
            self.parser = parser.WorldCommandParser()
        elif self.mode == const.modes.observe:
            self.parser = parser.ViewingCommandParser()
        elif self.mode == const.modes.chat:
            self.parser = parser.BanalityCommandParser()
        # XXX pass the User instance to the playerClass once the User class is
        # finished
        self.player = playerClass()
        self.parser.game = self

    def parseCommand(self, input):
        return self.parser.parseCommand(input)

    def setInterpreter(self, interpreter):
        """
        This is inteded to be called by gameshell.Manhole.setInterpreter.
        """
        self.interpreter = interpreter

    def updateActiveUsers(self, username):
        pass

    def getUserTerminal(self, username):
        # XXX lookup user data, return user.terminal

    def getUserRoles(self, username):
        # XXX lookup user data, return user.roles

    def sendUserMessage(self, username, message):
        self.getUserTerminal().write(message)



class SingleUserGame(Game):
    """
    """
    def __init__(self, *args, **kwargs):
        super(SingleUserGame, self).__init__(*args, **kwargs)
        self.activeUsername = ""
        self.activeSession = ""
        self.activeUserRoles = ""

    def updateActiveUsers(self, username):
        self.activeUsername = username


class MultiUserGame(Game):
    """
    """
    def updateActiveUsers(self, username):
        # XXX update the users collection in mongodb
        # XXX for each user, the game will need:
        #   * a reference to their session (so that it can write messages to
        #     the players)
        #   * the roles that this user has permissions to exercise (probably a
        #     database lookup)
        pass