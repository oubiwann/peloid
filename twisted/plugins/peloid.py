from twisted.application.service import ServiceMaker


PeloidMUDServer = ServiceMaker(
    "PeloidMUD Server",
    "dreammud.app.service",
    "A Twisted Python MUD Server ...",
    "dreammud")
