import sys

from twisted.application import service, internet
from twisted.python import usage

from dreamssh.sdk import const, interfaces, registry, scripts

from dreammud import config, meta
from dreammud.app.shell.service import getGameShellFactory


config = registry.getConfig()


class SubCommandOptions(usage.Options):
    """
    A base class for subcommand options.

    Can also be used directly for subcommands that don't have options.
    """


class Options(usage.Options):
    """
    """
    subCommands = [
        [const.KEYGEN, None, SubCommandOptions,
         "Generate ssh keys for the server"],
        [const.SHELL, None, SubCommandOptions, "Login to the server"],
        [const.STOP, None, SubCommandOptions, "Stop the server"],
        ]

    def parseOptions(self, options):
        config = registry.getConfig()
        usage.Options.parseOptions(self, options)
        # check options
        if self.subCommand == const.KEYGEN:
            scripts.KeyGen()
            sys.exit(0)
        elif self.subCommand == const.SHELL:
            scripts.ConnectToShell()
            sys.exit(0)
        elif self.subCommand == const.STOP:
            scripts.StopDaemon()
            sys.exit(0)


def makeService(options):
    # primary setup
    application = service.Application(meta.description)
    services = service.IServiceCollection(application)
    # setup ssh for the game server
    sshFactory = getGameShellFactory(app=application, services=services)
    sshServer = internet.TCPServer(config.ssh.port, sshFactory)
    sshServer.setName(config.ssh.servicename)
    sshServer.setServiceParent(services)
    # setup telnet for creating user accounts
    #telnetFactory = getSetupShellFactory()
    #telnetServer = internet.TCPServer(config.telnet.port, telnetFactory)
    #telnetServer.setName(config.telnet.servicename)
    #telnetServer.setServiceParent(services)
    return services
