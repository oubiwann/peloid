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
                 .                   |
                 .             Hall of Halls
                 .
            Shell Portal


    From these rooms, one is able to interact with the game world in several
    different and separate ways.

    If a player has system rights, a shell portal will be added as an exit. The
    shell portal will dump the player into the PeloidMUD shell interface.

    When a player leaves one world for another (or leaves the PeloidMUD shell
    for a world), the namespace that one is leaving needs to be saved and
    stored; the new world's namespace needs to be used instead. When the new
    world is left/exited, and the old one returned to, the old namespace needs
    to be restored.
    """
    graph = {}