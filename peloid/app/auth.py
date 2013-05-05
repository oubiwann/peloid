from twisted.conch import checkers
from twisted.cred import portal


class SSHPublicKeyDatabase(checkers.SSHPublicKeyDatabase):
    """
    """


class SSHPortal(portal.Portal):
    """
    """
    def __init__(self, *args, **kwargs):
        portal.Portal.__init__(self, *args, **kwargs)
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
