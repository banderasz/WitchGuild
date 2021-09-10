import unittest

from src.Table import Table
from src.Tile import TileType, Tile


class TestTable(unittest.TestCase):

    def setUp(self) -> None:
        self.table = Table()

    def test_init(self):
        position_0 = set()
        self.assertEqual(len(self.table.tiles), 36)
        for tile in self.table.tiles:
            if tile.ring == -1:
                tile.players.add(None)
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
        self.assertSetEqual({4, 8}, {first_tile.distance_to(pos0_tile) for pos0_tile in position_0})

    def test_get_center(self):
        self.assertEqual(TileType.TOWN, self.table.get_center().tile_type)

    def test_need_refresh(self):
        tile1 = Tile(TileType.HERB, ring=1)
        tile1.resource = 0
        self.table.tiles = {tile1}
        self.table.tiles.add(Tile(TileType.CRYSTAL, ring=3))
        self.table.tiles.add(Tile(TileType.SPIDER_WEB, ring=3))
        self.table.tiles.add(Tile(TileType.MUSHROOM, ring=3))
        self.table.tiles.add(Tile(TileType.BAT_WING, ring=3))
        self.assertTrue(self.table.need_refresh())

        self.table.tiles.add(Tile(TileType.HERB, ring=3))
        self.assertFalse(self.table.need_refresh())

    def test_nearest_town(self):
        tile_1 = None
        tile_2 = None
        tile_3 = None
        for tile in self.table.tiles:
            if tile.ring == 1:
                tile_1 = tile
            elif tile.ring == 2:
                tile_2 = tile
            elif tile.ring == 3:
                tile_3 = tile
            if tile_1 and tile_2 and tile_3:
                break
        self.assertEqual(1, self.table.nearest_town(tile_1).distance_to(tile_1))
        self.assertEqual(2, self.table.nearest_town(tile_2).distance_to(tile_2))
        self.assertEqual(3, self.table.nearest_town(tile_3).distance_to(tile_3))
