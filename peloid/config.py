from ConfigParser import SafeConfigParser
import os

from zope.interface import moduleProvides

from carapace.config import Config, Configurator, main, ssh
from carapace.sdk import interfaces

from peloid import meta


moduleProvides(interfaces.IConfig)


# Main
main.config.datadir = os.path.expanduser("~/.%s" % meta.library_name)
main.config.localfile = "config.ini"
main.config.installedfile = os.path.join(
    main.config.datadir, main.config.localfile)

# Database
db.name = "peloid"
db.usercollection = "user-data"
db.gamecollection = "game-data"

# SSH Server for game
ssh.servicename = meta.description
ssh.port = 4222
ssh.keydir = os.path.join(main.config.datadir, "ssh")
ssh.userdirtemplate = os.path.join(main.config.datadir, "users", "{{USER}}")
ssh.userauthkeys = os.path.join(ssh.userdirtemplate, "authorized_keys")
ssh.banner = """:
: Welcome to
: ____        ___                   __           __  __  ____
:/\  _`\     /\_ \           __    /\ \  /'\_/`\/\ \/\ \/\  _`\\
:\ \ \L\ \ __\//\ \     ___ /\_\   \_\ \/\      \ \ \ \ \ \ \/\ \\
: \ \ ,__/'__`\\\\ \ \   / __`\/\ \  /'_` \ \ \__\ \ \ \ \ \ \ \ \ \\
:  \ \ \/\  __/ \_\ \_/\ \L\ \ \ \/\ \L\ \ \ \_/\ \ \ \_\ \ \ \_\ \\
:   \ \_\ \____\/\____\ \____/\ \_\ \___,_\ \_\\\\ \_\ \_____\ \____/
:    \/_/\/____/\/____/\/___/  \/_/\/__,_ /\/_/ \/_/\/_____/\/___/
:
: You have entered a PeloidMUD Server.
: {{HELP}}
:
: Enjoy!
:
"""

# Telnet server for account creation
telnet = Config()
telnet.servicename = "Telnet Server"
telnet.ip = ssh.ip
telnet.port = ssh.port - 1
telnet.banner = """
Welcome to
  ____        ___                   __           __  __  ____
 /\  _`\     /\_ \           __    /\ \  /'\_/`\/\ \/\ \/\  _`\\
 \ \ \L\ \ __\//\ \     ___ /\_\   \_\ \/\      \ \ \ \ \ \ \/\ \\
  \ \ ,__/'__`\\\\ \ \   / __`\/\ \  /'_` \ \ \__\ \ \ \ \ \ \ \ \ \\
   \ \ \/\  __/ \_\ \_/\ \L\ \ \ \/\ \L\ \ \ \_/\ \ \ \_\ \ \ \_\ \\
    \ \_\ \____\/\____\ \____/\ \_\ \___,_\ \_\\\\ \_\ \_____\ \____/
     \/_/\/____/\/____/\/___/  \/_/\/__,_ /\/_/ \/_/\/_____/\/___/

You have connected to a Peloid registration server.

"""
telnet.registration = """
------------------------------------------------------------------------------
  "register <email@address> <SSH keys URL>" sets up an ssh account for you.
  "who" tells you who is logged in to the game.
  "quit" signs you off of the registration server.
  "help" gives help on the commands, "help commands" for a list.
------------------------------------------------------------------------------

"""
telnet.prompt = "> "
telnet.bye = "\n\nQuitting registration server...\nGood-bye!\n\n"


class PeloidMUDConfigurator(Configurator):
    """
    """
    def __init__(self, main, ssh, telnet):
        super(PeloidMUDConfigurator, self).__init__(main, ssh)
        self.db = db
        self.telnet = telnet

    def buildDefaults(self):
        config = super(PeloidMUDConfigurator, self).buildDefaults()
        config.add_section("Database")
        config.set("Database", "name", self.db.name)
        config.set("Database", "usercollection", self.db.usercollection)
        config.set("Database", "gamecollection", self.db.gamecollection)
        config.add_section("Telnet")
        config.set("Telnet", "servicename", self.telnet.servicename)
        config.set("Telnet", "ip", self.telnet.ip)
        config.set("Telnet", "port", str(self.telnet.port))
        return config

    def updateConfig(self):
        config = super(PeloidMUDConfigurator, self).updateConfig()
        if not config:
            return
        # Database
        db = self.db
        db.name = config.get("Database", "name")
        db.usercollection = config.get("Database", "usercollection")
        db.gamecollection = config.get("Database", "gamecollection")
        # Telnet
        telnet = self.telnet
        telnet.servicename = config.get("Telnet", "servicename")
        telnet.ip = config.get("Telnet", "ip")
        telnet.port = int(config.get("Telnet", "port"))
        return config


def configuratorFactory():
    return PeloidMUDConfigurator(main, ssh, telnet)


def updateConfig():
    configurator = configuratorFactory()
    configurator.updateConfig()
