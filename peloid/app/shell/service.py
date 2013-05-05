from twisted.cred import portal
from twisted.conch.checkers import SSHPublicKeyDatabase

from carapace.util import ssh as util

from peloid import const
from peloid.app.mud import game
from peloid.app.shell import gameshell, setupshell


def getGameShellFactory(gameFile=None, **namespace):
    """
    The "namespace" kwargs here contains the passed objects that will be
    accessible via the shell, namely:
     * "app"
     * "services"

    These two are passed in the call to peloid.app.service.makeService.
    """
    # XXX can we determine level of permission a user will have at this point?
    # XXX if so, we need to only use shell mode for those with system-level
    # perms, and hall of halls for everyone else... except anonymous users: they
    # can get dumped into hall of observing...
    gameInstance = game.Game(gameFile)
    gameInstance.setMode(const.modes.shell)
    sshRealm = gameshell.TerminalRealm(namespace, gameInstance)
    sshPortal = portal.Portal(sshRealm)
    factory = gameshell.GameShellFactory(sshPortal)
    factory.privateKeys = {'ssh-rsa': util.getPrivKey()}
    factory.publicKeys = {'ssh-rsa': util.getPubKey()}
    factory.portal.registerChecker(SSHPublicKeyDatabase())
    return factory


def getSetupShellFactory(**namespace):
    return setupshell.SetupShellServerFactory(namespace)