from twisted.python import log

from peloid import const


class Room(object):
    """
    """
    onEnterText = ""
    onExitText = ""
    exits = []

    def getDesc(self):
        return self.__doc__

    def getDescItems(self):
        """
        Describe the contents of the room.
        """
        # XXX do a database lookup for room contents, building a list of names
        msg = "There are no items worth examining here."
        return msg

    def getDescPlayers(self):
        """
        Get a list of players in the room.
        """
        # XXX do a database lookup for players in the room

    def getDescEnter(self):
        return self.onEnterText

    def getDescExit(self):
        return self.onExitText

    def getExitsText(self):
        exits = ", ".join(self.exits[:-1])
        return "This room has the following exits: %s, and %s." % (
            exits, self.exits[-1])

    def onEnter(self):
        pass

    def onOpenDoor(self):
        pass

    def onPassThreshold(self):
        pass

    def onEnter(self):
        pass

    def onExit(self):
        pass

    def enter(self):
        # XXX write getDescEnter to the user's shell
        self.onOpenDoor()
        self.onPassThreshold()
        self.onEnter()

    def exit(self):
        # XXX write getDescExit to the user's shell
        self.onOpenDoor()
        self.onPassThreshold()
        self.onExit()


class Hall(Room):
    """
    """


class HallOfHalls(Hall):
    """
    """


class HallOfCreators(Hall):
    """
    """


class HallOfControllers(Hall):
    """
    """


class HallOfAvatars(Hall):
    """
    """


class HallOfViewing(Hall):
    """
    """


class HallOfBanality(Hall):
    """
    """