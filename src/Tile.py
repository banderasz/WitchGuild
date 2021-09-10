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

    def __str__(self):
        return str(self.value)


class Tile:
    def __init__(self, tile_type: TileType = TileType.TOWN, ring: int = 0, position: int = 0):
        self.players = set()
        self.tile_type = tile_type
        self.ring = ring
        self.neighbours = set()
        self.resource = ring
        self.position = position

    def __str__(self):
        return "{}, {}".format(self.ring, self.position)

    def distance_to2(self, tile: 'Tile', distance: int = 0, visited: set = None) -> Optional[int]:
        if tile.players:
            return None
        visited = visited or set()
        visited.add(self)
        if tile in self.neighbours:
            return distance + 1
        for neighbour in self.neighbours:
            if neighbour not in visited and not neighbour.players:
                neighbour_distance = neighbour.distance_to(tile, distance + 1, visited)
                if neighbour_distance:
                    return neighbour_distance
        return None

    def distance_to(self, tile: 'Tile', distance=0, visited=None):
        visited = []
        queue = [self]
        self.distance = 0
        while queue:
            node = queue.pop(0)
            if tile in node.neighbours:
                return node.distance + 1
            if node not in visited:
                visited.append(node)
                for neighbour in node.neighbours:
                    if not neighbour.players:
                        neighbour.distance = node.distance + 1
                        queue.append(neighbour)
        return None


    def add_neighbour(self, tile: 'Tile') -> None:
        self.neighbours.add(tile)
        tile.neighbours.add(self)

    def get_token(self):
        if self.tile_type == TileType.TOWN:
            return None
        return ResourceType(self.tile_type.value)

    def gather(self):
        gathered = sum(np.random.randint(1, 7, self.ring * 2) > 4)
        if gathered > self.resource:
            gathered = self.resource
        self.resource -= gathered
        return gathered
