from typing import Set

import numpy as np
import networkx as nx
from matplotlib import pyplot as plt

from src.ResourceType import ResourceType
from src.Tile import Tile, TileType


class Table:
    def __init__(self):
        self.tiles: Set[Tile] = set()
        self.create_table()

    def create_table(self):
        middle_town = Tile(TileType.TOWN, ring=-1)
        self.tiles.add(middle_town)
        for i in range(5):
            town = Tile(TileType.TOWN, position=i)
            town.add_neighbour(middle_town)
            self.tiles.add(town)

        resource_sequence = [TileType(i + 1) for i in range(5)] * 6
        np.random.shuffle(resource_sequence)

        def create_ring_1_tile(offset=0):
            inner_tile = Tile(resource_sequence.pop(), 1, i)
            inner_tile.add_neighbour(middle_tile)
            for tile in self.tiles:
                if tile.ring == 0 and len(tile.neighbours) < 3 and (tile.position - inner_tile.position) % 5 == offset:
                    tile.add_neighbour(inner_tile)
                    break
            self.tiles.add(inner_tile)

        for i in range(5):
            middle_tile = Tile(resource_sequence.pop(), 2, i)

            create_ring_1_tile()
            create_ring_1_tile(1)

            for _ in range(3):
                outer_tile = Tile(resource_sequence.pop(), 3, i)
                outer_tile.add_neighbour(middle_tile)
                self.tiles.add(outer_tile)
            self.tiles.add(middle_tile)

    def get_center(self) -> Tile:
        for tile in self.tiles:
            if tile.ring == -1:
                return tile

    def need_refresh(self) -> bool:
        resources = {resource: 0 for resource in ResourceType}
        for tile in self.tiles:
            resources[tile.get_token()] += tile.resource
        return not all(resources.values())

    def nearest_town(self, tile):
        return sorted([(town, tile.distance_to(town)) for town in self.tiles if town.tile_type == TileType.TOWN]
                      , key=lambda x: x[1])[0][0]

    def visualize_table(self):
        G = nx.Graph()
        for tile in self.tiles:
            G.add_edges_from([(tile, neighbour) for neighbour in tile.neighbours])
        nx.draw_networkx(G)
        plt.show()

    def get_all_of_type(self, tile_type: TileType):
        return [tile for tile in self.tiles if tile.tile_type == tile_type]
