import sys

from twisted.application import service, internet
from twisted.python import usage

from carapace.sdk import const as sshConst, interfaces, registry, scripts

from peloid import config, const, meta
from peloid.app.shell.service import getGameShellFactory, getSetupShellFactory


config = registry.getConfig()


class SubCommandOptions(usage.Options):
    """
    A base class for subcommand options.

    Can also be used directly for subcommands that don't have options.
    """


class Options(usage.Options):
    """
    """
    optParameters = [
        [const.gamefileLongOption, const.gamefileShortOption, None,
         ("The game file for the game you wish to run in PeloidMUD.")]
        ]
    subCommands = [
        [sshConst.KEYGEN, None, SubCommandOptions,
         "Generate ssh keys for the server"],
        [sshConst.SHELL, None, SubCommandOptions, "Login to the server"],
        [sshConst.STOP, None, SubCommandOptions, "Stop the server"],
        ]

    def parseOptions(self, options):
        config = registry.getConfig()
        usage.Options.parseOptions(self, options)
        # check options
        if self.subCommand == sshConst.KEYGEN:
            scripts.KeyGen()
            sys.exit(0)
        elif self.subCommand == sshConst.SHELL:
            scripts.ConnectToShell()
            sys.exit(0)
        elif self.subCommand == sshConst.STOP:
            scripts.StopDaemon()
            sys.exit(0)


def makeService(options):
    # options
    gameFile = options.get(const.gamefileLongOption)

    # primary setup
    application = service.Application(meta.description)
    services = service.IServiceCollection(application)
    # setup ssh for the game server
    sshFactory = getGameShellFactory(
        gameFile=gameFile, app=application, services=services)
    sshServer = internet.TCPServer(config.ssh.port, sshFactory)
    sshServer.setName(config.ssh.servicename)
    sshServer.setServiceParent(services)
    # setup telnet for creating user accounts
    telnetFactory = getSetupShellFactory()
    telnetServer = internet.TCPServer(config.telnet.port, telnetFactory)
    telnetServer.setName(config.telnet.servicename)
    telnetServer.setServiceParent(services)
    # set up smtp for sending out registration emails
    # XXX add code
    # set up http for verifying registration from emails
    # XXX add code
    return services
