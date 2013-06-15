from twisted.trial import unittest

from peloid import const
from peloid.app.mud import game, parser


class CommandParserTestCase(unittest.TestCase):
    """
    """
    def setUp(self):
        self.parser = parser.CommandParser()
        # next we need to set the game attribute like a running mud server
        # would have done:
        self.parser.game = game.Game()
        self.parser.game.setMode(const.modes.lobby)

    def test_init(self):
        self.assertEqual(self.parser.command, None)
        self.assertEqual(self.parser.rest, None)
        self.assertEqual(self.parser.result, None)

    def test_prepCommandNoInput(self):
        self.parser.prepCommand()
        self.assertEqual(self.parser.command, [])
        self.assertEqual(self.parser.rest, [])

    def test_prepCommandSingle(self):
        self.parser.prepCommand("word")
        self.assertEqual(self.parser.command, "word")
        self.assertEqual(self.parser.rest, [])

    def test_prepCommandTwo(self):
        self.parser.prepCommand("two words")
        self.assertEqual(self.parser.command, "two")
        self.assertEqual(self.parser.rest, ["words"])

    def test_prepCommandMultiple(self):
        self.parser.prepCommand("here are more words still")
        self.assertEqual(self.parser.command, "here")
        self.assertEqual(self.parser.rest, ['are', 'more', 'words', 'still'])

    def test_parseHelp(self):
        self.parser.parseCommand("help")
        self.assertEqual(self.parser.command, "help")
        self.assertEqual(self.parser.rest, [])
        self.assertEqual(
            self.parser.result,
            "\n: This parser does not yet have 'help' information.")

    def test_parseEmote(self):
        self.parser.parseCommand("me looks at his watch")
        self.assertEqual(self.parser.result, "None looks at his watch")

    def test_badCommand(self):
        self.parser.parseCommand("wassup")
        self.assertEqual(self.parser.result, parser.commandError)


class ShellCommandParser(CommandParserTestCase):
    """
    """
    def setUp(self):
        self.parser = parser.ShellCommandParser()
        # next we need to set the game attribute like a running mud server
        # would have done:
        self.parser.game = game.Game()
        self.parser.game.setMode(const.modes.shell)

    def test_parseEnter(self):
        self.assertEqual(self.parser.game.mode, const.modes.shell)
        self.parser.parseCommand("enter")
        self.assertEqual(self.parser.game.mode, const.modes.lobby)