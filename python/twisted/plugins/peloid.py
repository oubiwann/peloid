from twisted.application.service import ServiceMaker


PeloidMUDServer = ServiceMaker(
    "PeloidMUD Server",
    "peloid.app.service",
    "A Twisted Python MUD Server ...",
    "peloid")
