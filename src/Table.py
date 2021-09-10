import numpy as np

from src.Tile import Tile, TileType


class Table:
    def __init__(self):
        self.tiles = set()
        self.create_table()

    def create_table(self):
        middle_town = Tile(TileType.TOWN, position=-1)
        self.tiles.add(middle_town)
        for _ in range(5):
            town = Tile(TileType.TOWN)
            town.add_neighbour(middle_town)
            self.tiles.add(town)

        resource_sequence = [TileType(i+1) for i in range(5)]*6
        np.random.shuffle(resource_sequence)

        for _ in range(5):
            middle_tile = Tile(resource_sequence.pop(), 2)
            for _ in range(2):
                inner_tile = Tile(resource_sequence.pop(), 1)
                inner_tile.add_neighbour(middle_tile)
                for tile in self.tiles:
                    if tile.position == 0 and len(tile.neighbours) < 3:
                        tile.add_neighbour(inner_tile)
                        break
                self.tiles.add(inner_tile)
            for _ in range(3):
                outer_tile = Tile(resource_sequence.pop(), 3)
                outer_tile.add_neighbour(middle_tile)
                self.tiles.add(outer_tile)
            self.tiles.add(middle_tile)


