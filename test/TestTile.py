import unittest

from src.Tile import Tile, TileType


class TestTile(unittest.TestCase):

    def setUp(self) -> None:
        self.tile1 = Tile()
        self.tile2 = Tile()
        self.tile3 = Tile(TileType.HERB)
        self.tile4 = Tile(TileType.MUSHROOM)
        self.tile5 = Tile(TileType.CRYSTAL)
        self.tile6 = Tile(TileType.SPIDER_WEB)

    def test_neighbours_added_to_both(self):
        self.tile1.add_neighbour(self.tile2)
        self.assertIn(self.tile2, self.tile1.neighbours)
        self.assertIn(self.tile1, self.tile2.neighbours)

    def test_difference_between_tiles(self):
        self.tile1.add_neighbour(self.tile2)
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
