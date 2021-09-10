from enum import Enum
from typing import Optional


class TileType(Enum):
    BAT_WING = 1
    SPIDER_WEB = 2
    CRYSTAL = 3
    HERB = 4
    MUSHROOM = 5
    TOWN = 6


class Tile:
    def __init__(self, tile_type: TileType = TileType.TOWN):
        self.tile_type = tile_type
        self.neighbours = set()

    def distance_to(self, tile: 'Tile', distance: int = 0, visited: set = None) -> Optional[int]:
        visited = visited or set()
        visited.add(self)
        if tile in self.neighbours:
            return distance + 1
        for neighbour in self.neighbours:
            if neighbour not in visited:
                neighbour_distance = neighbour.distance_to(tile, distance + 1, visited)
                if neighbour_distance:
                    return neighbour_distance
        return None

    def add_neighbour(self, tile: 'Tile') -> None:
        self.neighbours.add(tile)
        tile.neighbours.add(self)
