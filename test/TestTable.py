import unittest

from src.Table import Table
from src.Tile import TileType


class TestTable(unittest.TestCase):

    def setUp(self) -> None:
        self.table = Table()

    def test_init(self):
        position_0 = set()
        self.assertEqual(len(self.table.tiles), 36)
        for tile in self.table.tiles:
            if tile.ring == -1:
                tile.free = False
                self.assertEqual(5, len(tile.neighbours))
                self.assertEqual(TileType.TOWN, tile.tile_type)
            elif tile.ring == 0:
                position_0.add(tile)
                self.assertEqual(3, len(tile.neighbours))
                self.assertEqual(TileType.TOWN, tile.tile_type)
            elif tile.ring == 1:
                self.assertEqual(2, len(tile.neighbours))
                self.assertNotEqual(TileType.TOWN, tile.tile_type)
            elif tile.ring == 2:
                self.assertEqual(5, len(tile.neighbours))
                self.assertNotEqual(TileType.TOWN, tile.tile_type)
            elif tile.ring == 3:
                self.assertEqual(1, len(tile.neighbours))
                self.assertNotEqual(TileType.TOWN, tile.tile_type)
        first_tile = position_0.pop()
        self.assertSetEqual({4, 8, 12, 16}, {first_tile.distance_to(pos0_tile) for pos0_tile in position_0})
