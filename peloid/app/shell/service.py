from twisted.cred import portal
from twisted.conch import manhole_ssh
from twisted.conch.checkers import SSHPublicKeyDatabase

from carapace.util import ssh as util

from peloid.app.shell import gameshell, setupshell


def getGameShellFactory(**namespace):
    game = None
    sshRealm = gameshell.TerminalRealm(namespace, game)
    sshPortal = portal.Portal(sshRealm)
    factory = manhole_ssh.ConchFactory(sshPortal)
    factory.privateKeys = {'ssh-rsa': util.getPrivKey()}
    factory.publicKeys = {'ssh-rsa': util.getPubKey()}
    factory.portal.registerChecker(SSHPublicKeyDatabase())
    return factory


def getSetupShellFactory(**namespace):
    #telnetRealm = setupshell.X
    #telnetPortal = portal.Portal(telnetRealm)
    pass
