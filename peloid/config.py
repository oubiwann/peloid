from ConfigParser import SafeConfigParser
import os

from zope.interface import moduleProvides

from carapace.config import Config, Configurator, main, ssh
from carapace.sdk import interfaces

from dreammud import meta


moduleProvides(interfaces.IConfig)


main.config.datadir = os.path.expanduser("~/.%s" % meta.library_name)
main.config.localfile = "config.ini"
main.config.installedfile = os.path.join(
    main.config.datadir, main.config.localfile)

# SSH Server for game
ssh.servicename = meta.description
ssh.port = 4222
ssh.keydir = os.path.join(main.config.datadir, "ssh")
ssh.userdirtemplate = os.path.join(main.config.datadir, "users", "{{USER}}")
ssh.userauthkeys = os.path.join(ssh.userdirtemplate, "authorized_keys")
ssh.banner = """:
: Welcome to
:
:   ____                                              __  __  ____
:  /\  _`\                                    /'\_/`\/\ \/\ \/\  _`\\
:  \ \ \/\ \  _ __    __     __      ___ ___ /\      \ \ \ \ \ \ \/\ \\
:   \ \ \ \ \/\`'__\/'__`\ /'__`\  /' __` __`\ \ \__\ \ \ \ \ \ \ \ \ \\
:    \ \ \_\ \ \ \//\  __//\ \L\.\_/\ \/\ \/\ \ \ \_/\ \ \ \_\ \ \ \_\ \\
:     \ \____/\ \_\\\\ \____\ \__/.\_\ \_\ \_\ \_\ \_\\\\ \_\ \_____\ \____/
:      \/___/  \/_/ \/____/\/__/\/_/\/_/\/_/\/_/\/_/ \/_/\/_____/\/___/
:
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


class PeloidMUDConfigurator(Configurator):
    """
    """
    def __init__(self, main, ssh, telnet):
        super(PeloidMUDConfigurator, self).__init__(main, ssh)
        self.telnet = telnet

    def buildDefaults(self):
        config = super(PeloidMUDConfigurator, self).buildDefaults()
        config.add_section("Telnet")
        config.set("Telnet", "servicename", self.telnet.servicename)
        config.set("Telnet", "ip", self.telnet.ip)
        config.set("Telnet", "port", str(self.telnet.port))
        return config

    def updateConfig(self):
        config = super(PeloidMUDConfigurator, self).updateConfig()
        if not config:
            return
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
