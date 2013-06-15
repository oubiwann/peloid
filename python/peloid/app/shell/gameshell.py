from twisted.conch import manhole_ssh

from carapace.app.shell import base
from carapace.sdk import interfaces, registry

from peloid import util
from peloid.app import auth


config = registry.getConfig()

noGameWorldLoginWarningTemplate = """

 WARNING! You seem to have not provided a game file with a command-line
 option. To create a new world, enter the Hall of Creators.
"""


class SessionTransport(base.TerminalSessionTransport):
    """
    """
    def sessionInit(self):
        # XXX this method isn't used yet ... see the following tickets:
        #  * https://github.com/oubiwann/peloid/issues/32
        #  * https://github.com/oubiwann/carapace/issues/3
        # XXX do a db lookup to get roles
        roles = []
        user = auth.User(self.username, self.terminal, roles)
        self.game.updateActiveUsers(user)

    def writeMOTD(self):
        # XXX once termProto and self.terminal are set in the super class, we
        # can remove them from here
        termProto = self.chainedProtocol.terminalProtocol
        self.terminal = termProto.terminal
        motd = config.ssh.banner.replace("{{HELP}}", self.getHelpHint())
        motd = motd.replace("{{WELCOME}}", self.getWelcome())
        self.terminal.write("\r\n" + motd + "\r\n")
        self.terminal.write(termProto.ps[termProto.pn])

    def getWelcome(self):
        return config.ssh.welcome.replace("{{NAME}}", self.username)

    def getHelpHint(self):
        parser = self.game.parser
        msg = parser.getHelp()
        # XXX there's no actual check here for a running world
        if self.game:
            msg += noGameWorldLoginWarningTemplate.replace(
                "\n", parser.getNewline())
        return msg


class TerminalSession(base.ExecutingTerminalSession):
    """
    """
    transportFactory = SessionTransport

    def _processShellCommand(self, cmd, namespace):
        pass

    def openShell(self, proto):
        username = util.getUsernameFromAdaptor(self.original)
        self.transportFactory.username = username
        self.realm.setUsername(username)
        self.realm.getGame().updateActiveUsers(username)
        base.ExecutingTerminalSession.openShell(self, proto)


class TerminalRealm(base.ExecutingTerminalRealm):
    """
    """
    sessionFactory = TerminalSession
    transportFactory = SessionTransport

    def __init__(self, namespace, game):
        self._peloid_game = game
        self._peloid_username = None
        base.ExecutingTerminalRealm.__init__(self, namespace)
        self.transportFactory.game = game
        self.sessionFactory.realm = self

        def getManhole(serverProtocol):
            return Manhole(game, namespace)

        self.chainedProtocolFactory.protocolFactory = getManhole

    def getGame(self):
        return self._peloid_game

    def setUsername(self, username):
        self._peloid_username = username


class Interpreter(base.Interpreter):
    """
    """
    def runsource(self, input, filename):
        #self.write("input = %s, filename = %s" % (input, filename))
        self.write(str(self.game.parseCommand(input)))

    def setGame(self, game):
        self.game = game

    def updateNamespace(self, namespace={}):
        pass


class Manhole(base.MOTDColoredManhole):
    """
    """
    def __init__(self, game, namespace):
        base.MOTDColoredManhole.__init__(self, None, namespace)
        self.game = game
        self.game.start()


    def setInterpreter(self, klass=None, namespace={}):
        if namespace:
            self.updateNamespace(namespace)
        else:
            namespace = self.namespace
        self.interpreter = Interpreter(self, locals=namespace)
        self.interpreter.setGame(self.game)
        self.game.setInterpreter(self.interpreter)
        # now that we know what's writing the data for the game, we can
        # register the component
        registry.registerComponent(
            self.interpreter, interfaces.ITerminalWriter)

    def updateNamespace(self, namespace={}):
        self.interpreter.updateNamespace(namespace)


class GameShellFactory(manhole_ssh.ConchFactory):
    """
    """
