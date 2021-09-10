import unittest

from src.Player import Player
from src.ResourceType import ResourceType
from src.Tile import Tile, TileType


class TestTile(unittest.TestCase):

    def setUp(self) -> None:
        self.tile1 = Tile()
        self.tile2 = Tile()
        self.tile3 = Tile(TileType.HERB, 1)
        self.tile4 = Tile(TileType.MUSHROOM, 2)
        self.tile5 = Tile(TileType.CRYSTAL, 2)
        self.tile6 = Tile(TileType.SPIDER_WEB, 3)
        self.tile7 = Tile(TileType.BAT_WING, 1)

    def test_neighbours_added_to_both(self):
        self.tile1.add_neighbour(self.tile2)
        self.assertIn(self.tile2, self.tile1.neighbours)
        self.assertIn(self.tile1, self.tile2.neighbours)

    def test_difference_between_tiles(self):
        self.tile1.add_neighbour(self.tile2)
        self.tile1.add_neighbour(self.tile7)
        self.tile2.add_neighbour(self.tile3)
        self.tile3.add_neighbour(self.tile4)
        self.tile3.add_neighbour(self.tile5)
        self.tile5.add_neighbour(self.tile6)

        self.assertEqual(self.tile1.distance_to(self.tile6), 4)
        self.assertEqual(self.tile6.distance_to(self.tile1), 4)
        self.assertEqual(self.tile4.distance_to(self.tile5), 2)
        self.assertEqual(self.tile5.distance_to(self.tile4), 2)
        self.assertEqual(self.tile6.distance_to(self.tile4), 3)
        self.assertEqual(self.tile4.distance_to(self.tile6), 3)

    def test_get_token(self):
        self.assertIsNone(self.tile1.get_token())
        self.assertIsNone(self.tile2.get_token())
        self.assertEqual(self.tile3.get_token(), ResourceType.HERB)
        self.assertEqual(self.tile4.get_token(), ResourceType.MUSHROOM)
        self.assertEqual(self.tile5.get_token(), ResourceType.CRYSTAL)
        self.assertEqual(self.tile6.get_token(), ResourceType.SPIDER_WEB)

    def test_gather(self):
        for _ in range(1000):
            self.assertLessEqual(self.tile3.gather(), 1)
            self.assertLessEqual(self.tile4.gather(), 2)
            self.assertLessEqual(self.tile5.gather(), 3)
            self.assertLessEqual(self.tile6.gather(), 3)

            self.assertGreaterEqual(self.tile3.gather(), 0)
            self.assertGreaterEqual(self.tile4.gather(), 0)
            self.assertGreaterEqual(self.tile5.gather(), 0)
            self.assertGreaterEqual(self.tile6.gather(), 0)

    def test_tile_not_reachable(self):
        self.tile3.free = False
        self.assertIsNone(self.tile1.distance_to(self.tile6))
        self.assertIsNone(self.tile6.distance_to(self.tile1))
        self.assertIsNone(self.tile4.distance_to(self.tile5))
        self.assertIsNone(self.tile5.distance_to(self.tile4))

    def test_alternative_path(self):
        self.tile1.add_neighbour(self.tile2)
        self.tile2.add_neighbour(self.tile3)
        self.tile3.add_neighbour(self.tile4)
        self.tile3.add_neighbour(self.tile5)
        self.tile5.add_neighbour(self.tile6)

        self.tile2.players.add(None)
        tile_2a = Tile()
        self.tile1.add_neighbour(tile_2a)
        tile_2b = Tile()
        tile_2a.add_neighbour(tile_2b)
        tile_2b.add_neighbour(self.tile3)

        self.assertEqual(5, self.tile1.distance_to(self.tile6))
        self.assertEqual(5, self.tile6.distance_to(self.tile1))
        self.assertEqual(2, self.tile4.distance_to(self.tile5))
        self.assertEqual(2, self.tile5.distance_to(self.tile4))
        self.assertEqual(3, self.tile6.distance_to(self.tile4))
        self.assertEqual(3, self.tile4.distance_to(self.tile6))

