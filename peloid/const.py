class Organizer(object):
	pass


# Game Modes
modes = Organizer()
modes.lobby = 1
modes.create = 2
modes.controll = 3
modes.avatar = 4
modes.play = 5
modes.observe = 6
modes.chat = 7

# Game commands
cmds = Organizer()
cmds.look = ["look", "view", "observe"]
cmds.go = ["walk", "move", "go"]