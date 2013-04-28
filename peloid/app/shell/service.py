from twisted.cred import portal
from twisted.conch.checkers import SSHPublicKeyDatabase

from carapace.util import ssh as util

from peloid.app import mud
from peloid.app.shell import gameshell, setupshell


def getGameShellFactory(**namespace):
    """
    The "namespace" kwargs here contains the passed objects that will be
    accessible via the shell, namely:
     * "app"
     * "services"

    These two are passed in the call to peloid.app.service.makeService.
    """
    game = mud.Game()
    sshRealm = gameshell.TerminalRealm(namespace, game)
    sshPortal = portal.Portal(sshRealm)
    factory = gameshell.GameShellFactory(sshPortal)
    factory.privateKeys = {'ssh-rsa': util.getPrivKey()}
    factory.publicKeys = {'ssh-rsa': util.getPubKey()}
    factory.portal.registerChecker(SSHPublicKeyDatabase())
    return factory


def getSetupShellFactory(**namespace):
    return setupshell.SetupShellServerFactory(namespace)
