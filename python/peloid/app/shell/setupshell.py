from twisted.conch.telnet import TelnetProtocol, TelnetTransport
from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver

from carapace.sdk import interfaces, registry

from peloid.app import register


config = registry.getConfig()


class ExecutingShell(TelnetProtocol):
    """
    """
    def write(self, data):
        self.transport.write(str(data))

    def prompt(self):
        self.write(config.telnet.prompt)

    def dataReceived(self, data):
        self.execCommand(data.split())

    def _processShellCommand(self, cmd, args):
        raise NotImplementedError

    def execCommand(self, args):
        if not args:
            self.prompt()
            return
        cmd = args[0]
        params = args[1:]
        if not params:
            params = ["<no parameters passed>"]
        try:
            self._processShellCommand(cmd, params)
        except Exception, error:
            # debug XXX
            #self.write(error)
            commandInput = "%s %s" % (cmd, " ".join(params))
            errorParts = error.message.split()
            if errorParts[0].startswith("telnet_"):
                msg = ("\n" + errorParts[0].replace(
                    "telnet_", "").replace("()", " ") +
                    " ".join(errorParts[1:]) +
                    ". You typed:\n\n\t" +
                    commandInput + "\n\n" +
                    "To see a list of commands, type 'help'.\n\n")
            else:
                msg = "Command not understood.\n\n"
            self.write(msg)
            self.prompt()


class SetupShell(ExecutingShell):
    """
    """
    # XXX this class (or a parent class) needs to set some variables for
    # the services that are running on the server so that the game data can
    # be accesses, introspected, and reported upon
    def connectionMade(self):
        self.write(config.telnet.banner)
        self.telnet_help()

    def _processShellCommand(self, cmd, args):
        getattr(self, "telnet_%s" % cmd)(*args)

    def notifyWhenComplete(self, results):
        self.write("\n\nUser created successfully!\n\n")
        self.prompt()

    def reportError(self, reason):
        self.write("\n\nThere was an error: %s\n\n" % str(reason))

    def telnet_register(self, email, sshKeysURL):
        signUp = register.Registration(email, sshKeysURL)
        d = signUp.run()
        d.addCallback(self.notifyWhenComplete)
        d.addErrback(self.reportError)
        self.prompt()

    def telnet_who(self, *args):
        self.write("\n\nService not yet implemented.\n\n")

    def telnet_quit(self, *args):
        self.write(config.telnet.bye)
        self.transport.loseConnection()

    telnet_q = telnet_quit

    def telnet_help(self, *args):
        self.write(config.telnet.registration + "\n\n")
        self.prompt()

    telnet_h = telnet_help


class SetupShellTransport(TelnetTransport):
    """
    """
    protocolFactory = SetupShell


def buildSetupShellProtocol(factory):
    return SetupShellTransport(SetupShell)


class SetupShellServerFactory(ServerFactory):
    """
    """
    protocol = buildSetupShellProtocol

    def __init__(self, namespace, *args, **kwargs):
        self.namespace = namespace
