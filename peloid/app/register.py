import json

from twisted.internet.defer import DeferredList, maybeDeferred
from twisted.python import log
from twisted.web.client import getPage

from peloid.app.models.user import UserModel


class Registration(object):
    """
    """
    def __init__(self, email, sshKeysURL):
        self.email = email
        self.sshKeysURL = sshKeysURL

    def createUser(self, keys):
        # XXX check to see if the user exists
        # XXX if the user exists, raise an exception
        user = UserModel(email=self.email, sshKeys=keys)
        d = user.insert()
        d.addErrback(log.err)
        return d

    def _processGitHubKeys(self, results):
        data = json.loads(results)
        return [x.get("key") for x in data]

    def _processLPKeys(self, results):
        return [x for x in results.split("\n")]

    def processKeys(self, results):
        if "launchpad.net" in self.sshKeysURL:
            return self._processLPKeys(results)
        elif "github.com" in self.sshKeysURL:
            return self._processGitHubKeys(results)

    def getKeys(self):
        d = getPage(self.sshKeysURL)
        d.addCallback(self.processKeys)
        d.addErrback(log.err)
        return d

    def run(self):
        d = self.getKeys()
        d.addCallback(self.createUser)
        return d
