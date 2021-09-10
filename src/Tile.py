from enum import Enum
from typing import Optional
import numpy as np

from src.ResourceType import ResourceType


class TileType(Enum):
    BAT_WING = 1
    SPIDER_WEB = 2
    CRYSTAL = 3
    HERB = 4
    MUSHROOM = 5
    TOWN = 6


class Tile:
    def __init__(self, tile_type: TileType = TileType.TOWN, position: int = 0):
        self.tile_type = tile_type
        self.position = position
        self.neighbours = set()
        self.resource = position

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

    def get_token(self):
        if self.tile_type == TileType.TOWN:
            return None
        return ResourceType(self.tile_type.value)

    def gather(self):
        gathered = sum(np.random.randint(1, 7, self.position * 2) > 4)
        if gathered > self.resource:
            gathered = self.resource
        self.resource -= gathered
        return gathered
