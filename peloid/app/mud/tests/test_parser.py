from twisted.trial import unittest

from peloid.app.mud import parser


class CommandParserTestCase(unittest.TestCase):
    """
    """
    def setUp(self):
        self.parser = parser.CommandParser()

    def test_init(self):
        self.assertEqual(self.parser.command, None)
        self.assertEqual(self.parser.rest, None)
        self.assertEqual(self.parser.result, None)

    def test_prepCommandNoInput(self):
        self.parser.prepCommand()
        self.assertEqual(self.parser.command, [])
        self.assertEqual(self.parser.rest, [])