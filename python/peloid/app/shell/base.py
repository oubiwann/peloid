import os
from pprint import pprint
import sys

from twisted.conch import manhole, manhole_ssh
from twisted.python import log

from carapace.sdk import registry


config = registry.getConfig()
