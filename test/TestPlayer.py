import unittest

from src.Player import Player
from src.ResourceType import ResourceType
from src.Tile import Tile, TileType


class TestPlayer(unittest.TestCase):

    def setUp(self) -> None:
        self.player = Player()
        self.tile1 = Tile()
        self.tile2 = Tile()
        self.tile3 = Tile(TileType.HERB, 1)
        self.tile4 = Tile(TileType.MUSHROOM, 2)
        self.tile5 = Tile(TileType.CRYSTAL, 2)
        self.tile6 = Tile(TileType.SPIDER_WEB, 3)
        self.tile1.add_neighbour(self.tile2)
        self.tile2.add_neighbour(self.tile3)
        self.tile3.add_neighbour(self.tile4)
        self.tile3.add_neighbour(self.tile5)
        self.tile5.add_neighbour(self.tile6)
        self.player.tile = self.tile1

    def test_gathering_from_town(self):
        self.assertRaises(ValueError, self.player.gather)

    def test_gathering_from_not_town(self):
        self.player.tile = self.tile3
        for _ in range(1000):
            self.player.gather()
            self.assertLessEqual(self.player.resources[self.tile3.get_token()], self.tile3.position)
            self.assertGreaterEqual(self.player.resources[self.tile3.get_token()], 0)

    def test_hand_limit(self):
        self.player.resources[ResourceType.SPIDER_WEB] = 8
        self.player.tile = self.tile6
        for _ in range(1000):
            self.player.gather()
        self.assertEqual(10, self.player.sum_resources())
        self.assertEqual(0, self.tile6.resource)

    def test_moving(self):
        self.player.move_to(self.tile6)
        self.assertFalse(self.tile6.free)
        self.assertTrue(self.tile1.free)
        self.assertEqual(self.tile6, self.player.tile)
        self.assertEqual(1, self.player.actions)

