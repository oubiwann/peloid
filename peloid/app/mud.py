class World(object):
    pass


class Player(object):
    pass


class Game(object):
    """
    """
    def start(self, *args, **kwargs):
        pass

    def parseCommand(self, input):
        parts = input.lower().split()
        if parts[0] == "look":
            return "You look around..."
