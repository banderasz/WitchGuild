import unittest

from src.Table import Table
from src.Tile import TileType


class TestTile(unittest.TestCase):

    def setUp(self) -> None:
        self.table = Table()

    def test_init(self):
        self.assertEqual(len(self.table.tiles), 36)
        for tile in self.table.tiles:
            if tile.position == -1:
                self.assertEqual(5, len(tile.neighbours))
                self.assertEqual(TileType.TOWN, tile.tile_type)
            elif tile.position == 0:
                self.assertEqual(3, len(tile.neighbours))
                self.assertEqual(TileType.TOWN, tile.tile_type)
            elif tile.position == 1:
                self.assertEqual(2, len(tile.neighbours))
                self.assertNotEqual(TileType.TOWN, tile.tile_type)
            elif tile.position == 2:
                self.assertEqual(5, len(tile.neighbours))
                self.assertNotEqual(TileType.TOWN, tile.tile_type)
            elif tile.position == 3:
                self.assertEqual(1, len(tile.neighbours))
                self.assertNotEqual(TileType.TOWN, tile.tile_type)
