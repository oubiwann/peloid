from ConfigParser import SafeConfigParser
import os

from zope.interface import moduleProvides

from dreamssh.config import Config, Configurator, main, ssh
from dreamssh.sdk import interfaces

from dreammud import meta


moduleProvides(interfaces.IConfig)


main.config.userdir = os.path.expanduser("~/.%s" % meta.library_name)
main.config.localfile = "config.ini"
main.config.userfile = "%s/%s" % (main.config.userdir, main.config.localfile)

# Telnet server for account creation
telnet = Config()
telnet.servicename = "Telnet Server"
telnet.port = 4221

# SSH Server for game
ssh.servicename = meta.description
ssh.port = 4222
ssh.keydir = os.path.join(main.config.userdir, "ssh")
ssh.banner = """:
: Welcome to
:
:   ____                                              __  __  ____      
:  /\  _`\                                    /'\_/`\/\ \/\ \/\  _`\    
:  \ \ \/\ \  _ __    __     __      ___ ___ /\      \ \ \ \ \ \ \/\ \  
:   \ \ \ \ \/\`'__\/'__`\ /'__`\  /' __` __`\ \ \__\ \ \ \ \ \ \ \ \ \ 
:    \ \ \_\ \ \ \//\  __//\ \L\.\_/\ \/\ \/\ \ \ \_/\ \ \ \_\ \ \ \_\ \
:     \ \____/\ \_\\ \____\ \__/.\_\ \_\ \_\ \_\ \_\\ \_\ \_____\ \____/
:      \/___/  \/_/ \/____/\/__/\/_/\/_/\/_/\/_/\/_/ \/_/\/_____/\/___/ 
:                                                                              
:
: You have entered a DreamMUD Server.
: {{HELP}}
:
: Enjoy!
:
"""

class DreamMUDConfigurator(Configurator):
    """
    """
    def __init__(self, main, ssh, telnet):
        super(DreamMUDConfigurator, self).__init__(main, ssh)
        self.telnet = telnet

    def buildDefaults(self):
        config = super(DreamMUDConfigurator, self).buildDefaults()
        config.set("Telnet", "servicename", self.telnet.servicename)
        config.set("Telnet", "port", self.telnet.port)
        return config

    def updateConfig(self):
        config = super(DreamMUDConfigurator, self).updateConfig()
        telnet = self.telnet
        # Telnet
        telnet.servicename = config.get("Telnet", "servicename")
        telnet.nick = int(config.get("Telnet", "port"))
        return config


def updateConfig():
    configurator = DreamMUDConfigurator(main, ssh)
    configurator.updateConfig()
