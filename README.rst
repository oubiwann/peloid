Peloid (MUD) Server
===================

.. image:: resources/persona_oc_mudbath_by_cheshiresworld-small.jpg
   :target: http://cheshirecaterling.deviantart.com/art/Persona-OC-Mudbath-202009649

Running the MUD
---------------

First, install MongoDB for your system, then start it up::

    $ mongod

In another terminal, download the code::

    $ git clone https://github.com/oubiwann/peloid.git

Set up a virtual environment to run everything in::

    $ cd peloid
    $ make virtual-build

Fire up the MUD server::

    $ . .venv/test-build/bin activate
    (test-build) $ make daemon

Registering a Username
----------------------

Connect to the registration server::

    $ telnet 4221 your.mudhost.com

You will be greeted with the following::

    Connected to localhost.
    Escape character is '^]'.

    Welcome to
      ____        ___                   __           __  __  ____
     /\  _`\     /\_ \           __    /\ \  /'\_/`\/\ \/\ \/\  _`\
     \ \ \L\ \ __\//\ \     ___ /\_\   \_\ \/\      \ \ \ \ \ \ \/\ \
      \ \ ,__/'__`\\ \ \   / __`\/\ \  /'_` \ \ \__\ \ \ \ \ \ \ \ \ \
       \ \ \/\  __/ \_\ \_/\ \L\ \ \ \/\ \L\ \ \ \_/\ \ \ \_\ \ \ \_\ \
        \ \_\ \____\/\____\ \____/\ \_\ \___,_\ \_\\ \_\ \_____\ \____/
         \/_/\/____/\/____/\/___/  \/_/\/__,_ /\/_/ \/_/\/_____/\/___/

    You have connected to a Peloid registration server.


    ------------------------------------------------------------------------------
      "register <email@address> <SSH keys URL>" sets up an ssh account for you.
      "who" tells you who is logged in to the game.
      "quit" signs you off of the registration server.
      "help" gives help on the commands, "help commands" for a list.
    ------------------------------------------------------------------------------

    >

Now you can register::

    > register myemail@host.com https://launchpad.net/~mynick/+sshkeys

or::

    > register myemail@host.com https://api.github.com/users/mynick/keys


Logging in to the Game Server
-----------------------------

Once you have your ssh keys saved on the server (done automatically when you
register), you will be able to login::

    $ ssh -p 4222 your.mudhost.com

When you log into the Peloid MUD server right now, this is all you get::

    :>>
    :
    : Welcome to
    : ____        ___                   __           __  __  ____
    :/\  _`\     /\_ \           __    /\ \  /'\_/`\/\ \/\ \/\  _`\
    :\ \ \L\ \ __\//\ \     ___ /\_\   \_\ \/\      \ \ \ \ \ \ \/\ \
    : \ \ ,__/'__`\\ \ \   / __`\/\ \  /'_` \ \ \__\ \ \ \ \ \ \ \ \ \
    :  \ \ \/\  __/ \_\ \_/\ \L\ \ \ \/\ \L\ \ \ \_/\ \ \ \_\ \ \ \_\ \
    :   \ \_\ \____\/\____\ \____/\ \_\ \___,_\ \_\\ \_\ \_____\ \____/
    :    \/_/\/____/\/____/\/___/  \/_/\/__,_ /\/_/ \/_/\/_____/\/___/
    :
    : You have entered a PeloidMUD Server.
    : This shell has no commands; it simply returns what you type.
    :
    : Enjoy!
    :
    :>>

More soon!

Creating a Character
--------------------

TBD

Playing a Character
-------------------

TBD
