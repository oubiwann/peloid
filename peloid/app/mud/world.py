from twisted.python import log

from peloid import const


class World(object):
    """
    """


class MetaWorld(World):
    """
    The game metaworld contains the following rooms:


                                Game World
                                     |
              Hall of Contorllers    |    Hall of Viewing
                      |              |          |
    Hall of Creators  |      Hall of Avatars    |    Hall of Banality
            |         |              |          |           |
            |         |              |          |           |
            +---------+--------------+----------+-----------+
                                     |
                               Hall of Halls

    From these rooms, one is able to interact with the game world in several
    different and separate ways.

    When a player leaves one world for another (or leaves the PeloidMUD shell
    for a world), the namespace that one is leaving needs to be saved and
    stored; the new world's namespace needs to be used instead. When the new
    world is left/exited, and the old one returned to, the old namespace needs
    to be restored.
    """
    graph = {}