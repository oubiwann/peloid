from twisted.conch.telnet import TelnetProtocol, TelnetTransport
from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver

from carapace.sdk import interfaces, registry


config = registry.getConfig()


class ExecutingShell(TelnetProtocol):
    """
    """
    def write(self, data):
        self.transport.write(data)

    def prompt(self):
        self.write(config.telnet.prompt)

    def dataReceived(self, data):
        self.execCommand(data.split())

    def _processShellCommand(self, cmd, args):
        raise NotImplementedError

    def execCommand(self, args):
        cmd = args[0]
        params = args[1:]
        if not params:
            params = ["<no parameters passed>"]
        try:
            self._processShellCommand(cmd, params)
        except Exception, error:
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
    def connectionMade(self):
        self.write(config.telnet.banner)
        self.telnet_help()

    def _processShellCommand(self, cmd, args):
        getattr(self, "telnet_%s" % cmd)(*args)

    def telnet_register(self, email, sshKeysURL):
        self.write(
            "\n\nin telnet_register got: %s and %s\n\n" % (email, sshKeysURL))

    def telnet_who(self, *args):
        pass

    def telnet_quit(self, *args):
        self.write(dir(self))

    def telnet_help(self, *args):
        self.write(config.telnet.registration)
        self.prompt()


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
