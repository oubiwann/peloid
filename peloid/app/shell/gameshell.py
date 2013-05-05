from twisted.conch import manhole_ssh

from carapace.app.shell import base
from carapace.sdk import interfaces, registry

from peloid import util


config = registry.getConfig()

noGameWorldLoginWarningTemplate = """

 WARNING! You seem to have not provided a game file with a command-line
 option. To create a new world, enter the Hall of Creators.
"""


class SessionTransport(base.TerminalSessionTransport):
    """
    """
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
        base.ExecutingTerminalSession.openShell(self, proto)
        self.username = util.getUsernameFromAdaptor(self.original)


class TerminalRealm(base.ExecutingTerminalRealm):
    """
    """
    sessionFactory = TerminalSession
    transportFactory = SessionTransport

    def __init__(self, namespace, game):
        base.ExecutingTerminalRealm.__init__(self, namespace)
        self.transportFactory.game = game

        def getManhole(serverProtocol):
            return Manhole(game, namespace)

        self.chainedProtocolFactory.protocolFactory = getManhole


class Interpreter(base.Interpreter):
    """
    A simple interpreter that demonstrate where one can plug in any
    command-parsing shell.
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
