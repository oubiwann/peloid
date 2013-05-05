from twisted.conch import interfaces


def getUsernameFromAdaptor(adapter):
    avatar = interfaces.IConchUser(adapter)
    portal = avatar.conn.transport.factory.portal
    return portal.getUsername()