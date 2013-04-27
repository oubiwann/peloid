from zope.interface import Interface


class ICreator(Interface):
    """
    Roles that can add objects to game catalog or make significant changes to
    game maps.
    """


class ICraftsman(ICreator):
    """
    Can create furniture, books, clothing, orbs, weapons, and other game
    objects.
    """


class IArchitect(ICraftsman):
    """
    Can create buildings, dungeon rooms.
    """


class ITitan(IArchitect):
    """
    Can create new cities, dungeons, or dungeon levels.
    """


class IDeity(ITitan):
    """
    Can create maps, open areas (anything on a planetary, national, regional,
    or prefecture level).
    """


class IController(Interface):
    """
    Roles that can administer users, objects that exist in the game catalog,
    and in-game data.
    """


class IWizard(IController):
    """
    Can create objects, change objects, and teleport people.
    """


class IDruid(IController):
    """
    Can create natural objects and manipulate outdoor environments as well
    earthen structures (including minor modifications to dungeon rooms).
    """


class IInvoker(IController):
    """
    Can make changes to game rules.
    """


class IPsion(IController):
    """
    Can make changes to player stats, names, classes, etc.
    """
