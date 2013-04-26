import json

from twisted.internet.defer import DeferredList, maybeDeferred
from twisted.python import log
from twisted.web.client import getPage


class Registration(object):
    """
    """
    def __init__(self, email, sshKeysURL):
        self.email = email
        self.sshKeysURL = sshKeysURL

    def createUser(self):
        return maybeDeferred(lambda: "success")

    def processKeys(self, results):
        if "launchpad.net" in self.sshKeysURL:
            self._processLPKeys(results)
        elif "github.com" in self.sshKeysURL:
            self._processGitHubKeys(results)

    def _processGitHubKeys(self, results):
        data = json.loads(results)
        for keyData in data:
            log.msg(keyData.get("key"))

    def _processLPKeys(self, results):
        for line in results.split("\n"):
            log.msg(line)

    def getKeys(self):
        d = getPage(self.sshKeysURL)
        d.addCallback(self.processKeys)
        d.addErrback(log.err)
        return d

    def saveUserKeys(self, results):
        return maybeDeferred(lambda: "success")

    def run(self):
        d = DeferredList([
            self.getKeys(),
            self.createUser()])
        d.addCallback(self.saveUserKeys)
        d.addErrback(log.err)
        return d
