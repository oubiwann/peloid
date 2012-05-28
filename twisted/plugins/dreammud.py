from twisted.application.service import ServiceMaker


DreamMUDServer = ServiceMaker(
    "DreamMUD Server",
    "dreammud.app.service",
    "A Twisted Python MUD Server ...",
    "dreammud")
