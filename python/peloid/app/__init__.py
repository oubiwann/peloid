from carapace.sdk import registry

from peloid import config


config.updateConfig()
registry.registerConfig(config)
