from mongomodel import model

from carapace.sdk import const, interfaces, registry


config = registry.getConfig()


class UserModel(model.Model):
    db = config.db.name
    collection = config.db.usercollection
