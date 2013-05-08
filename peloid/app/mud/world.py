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

    Message directions:
      * world to room
      * world to player
      * room to player
      * player to room
      * player to player
      * player to group
      * group to player

    Keys that uniquely identify recipient (routing):
      * world:id:room:id
      * world:id:player:id
      * room:id:player:id
      * player:id:room:id
      * player:id:player:id
      * player:id:group:id
      * group:id:player:id

    Is it possible for the recipient to get both the key and the value? If so,
    then return messages simply have to invert the object:id pair.

    We probably also need keys for identifying the *type* of message being sent
    so that we can query for just the message types. Let's start wth an easy
    examples:
      * player:id:room:id:type:emote
      * player:id:player:id:type:whisper
      * room:id:player:id:type:content-change
      * room:id:player:id:type:player-left

    With all of this said, we know that:
      * Each object that can bethe source or destination of a message needs to
        be plugged into the world message bus.
      * This message bus *may* actually need to be span multiple worlds, so
        perhapds instead of "world message bus" we need "peloid message bus".
      * Each object needs a means of sending and receiving messages
      * Each object needs a means of writing data to the user's terminal
        session.

    As such, it looks like this docstring needs to be moved to a new "bus.py"
    module or something ;-)

    To keep data storage and messaging clearly defined and functionally
    separated, we probably need another module for data abstractions. This could
    go in a "data.py" module?

    Given that they are both going to be based on txRedis, there's a good chance
    they will share some common code, so a place should be made for that as
    well. So maybe:
      * peloid.app.data.common
      * peloid.app.data.bus
      * peloid.app.data.storage
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