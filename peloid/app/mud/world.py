from twisted.python import log

from peloid import const


class World(object):
    """
    The big question around how the world works is communication:
     * how do users/players in a room know that someone new has entered the
       room?
     * how does everyone in a room hear someone say something?
     * how does one user hear another user whisper to them?
     * how does a room know what contents it has?
     * when a user enters a room, what do they see or hear? How do they get this
       info/message(s)?

    The general answer to all of these is "messaging". Redis provides for both
    storage needs as well as Peloid's messaging needs, so we're uring the
    txRedis package. Redis is a key-value store, where keys can be arbitrarily
    constructed namespaces (in particular, strings with an arbitrary separator).

    Part of the design of Peloid's messaging system will be the definition of
    these keys, the parsing of them, the extraction of the associated values,
    and the planned routing for said messages.
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