from twisted.trial import unittest

from peloid.app.mud import room


class TestRoom(room.Room):
	"""
	You enter a dark room. You can see light between the planks comprising the
	floor. The air completely lacks in movement, seems half comprised of
	suspended dust, and smells of deep must. Whether or not it was intended
	originally, you can draw only one conclusion: this is now a test room.
	"""


class RoomTestCase(unittest.TestCase):
	"""
	"""
	def setUp(self):
		self.room = TestRoom()

	def test_getDesc(self):
		self.assertTrue(self.room.getDesc().startswith("\n\t"))
		self.assertTrue(self.room.getDesc().endswith("\n\t"))
		self.assertEqual(len(self.room.getDesc()), 293)
