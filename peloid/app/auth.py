from twisted.conch import checkers
from twisted.cred import portal


# XXX it might be better to unify this with the user model ...
class User(object):
    """
    """
    def __init__(self, username, terminal, roles):
        self.username = username
        self.terminal = terminal
        self.roles = roles


class SSHPublicKeyDatabase(checkers.SSHPublicKeyDatabase):
    """
    """


class SSHPortal(portal.Portal):
    """
    """
    def __init__(self, realm):
        portal.Portal.__init__(self, realm)
        self._peloid_realm = realm
        self._peloid_checker = None
        self._peloid_creds = None

    def getUsername(self):
        return self._peloid_creds.username

    def login(self, credentials, mind, *interfaces):
        self._peloid_creds = credentials
        return portal.Portal.login(self, credentials, mind, *interfaces)

    def registerChecker(self, checker):
        portal.Portal.registerChecker(self, checker)
        self._peloid_checker = checker
