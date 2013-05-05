from twisted.trial import unittest

from peloid.app.mud import room


class TestRoom(room.Room):
    """
    You enter a dark room. You can see light between the planks comprising the
    floor. The air completely lacks in movement, seems half comprised of
    suspended dust, and smells of deep must. Whether or not it was intended
    originally, you can draw only one conclusion: this is now a test room.
    """
    onEnterText = "A creaking door closes behind you."
    onExitText = "You breath deeply; the test room has passed."
    exits = ["W", "N", "E"]

    def __init__(self):
        self.testState = []

    def onOpenDoor(self):
        self.testState.append("door opened")

    def onPassThreshold(self):
        self.testState.append("passed through door")

    def onEnter(self):
        self.testState.append("entered room")

    def onExit(self):
        self.testState.append("exited room")


class RoomTestCase(unittest.TestCase):
    """
    """
    def setUp(self):
        self.room = TestRoom()

    def test_getDesc(self):
        self.assertTrue(self.room.getDesc().startswith("\n\t"))
        self.assertTrue(self.room.getDesc().endswith("\n\t"))
        self.assertEqual(len(self.room.getDesc()), 293)

    def test_getDescEnter(self):
        self.assertEqual(
            self.room.getDescEnter(),
            "A creaking door closes behind you.")

    def test_getDescExit(self):
        self.assertEqual(
            self.room.getDescExit(),
            "You breath deeply; the test room has passed.")

    def test_getExitsText(self):
        self.assertEqual(
            self.room.getExitsText(),
            "This room has the following exits: W, N, and E.")

    def test_enter(self):
        self.room.enter()
        self.assertEqual(
            self.room.testState,
            ['door opened', 'passed through door', 'entered room'])

    def test_exit(self):
        self.room.exit()
        self.assertEqual(
            self.room.testState,
            ['door opened', 'passed through door', 'exited room'])