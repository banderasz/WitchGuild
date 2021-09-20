import math
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


def k_out_of_n_probability(n: int, k: int, p: float) -> float:
    return math.comb(n, k) * p ** k * (1 - p) ** (n - k)


def at_least_k_out_of_n_probability(n: int, k: int, p: float) -> float:
    return sum([k_out_of_n_probability(n, dices, p) for dices in range(k, n + 1)])


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

    def expected_resource(self):
        p = 1 / 3
        expected_value = self.resource * at_least_k_out_of_n_probability(self.ring * 2, self.resource, p)
        for dices in range(1, self.resource):
            expected_value += dices * k_out_of_n_probability((self.ring * 2), dices, p)
        return expected_value

    def turns_to_collect(self, n: int) -> float:
        p = 1 / 3
        if n > self.resource:
            return np.inf
        if n == 1:
            x = at_least_k_out_of_n_probability(self.ring * 2, n, p)
            return 1 / x  # sum (n+1) * (1-x)^n * (x), n=0 to infinity
        if n == 2:
            x = at_least_k_out_of_n_probability(self.ring * 2, n, p)
            y = k_out_of_n_probability(self.ring * 2, 1, p)
            return (x + 2 * y) / (x + y) ** 2  # sum  (1-x-y)^n * ((n+1) * x +  y * (n+1+1/(x+y)) ), n=0 to infinity
        if n == 3:
            x = at_least_k_out_of_n_probability(self.ring * 2, n, p)
            y = k_out_of_n_probability(self.ring * 2, 2, p)
            z = k_out_of_n_probability(self.ring * 2, 1, p)
            return (x ** 2 + 3 * x * y + 3 * x * z + 2 * y ** 2 + 4 * y * z + 3 * z ** 2) \
                   / ((x + y + z) ** 3)  # sum  (1-x-y-z)^n * ((n+1) * x + y * (n+1+1/(x+y+z)) + z * ((((x+y) + 2z)/(
            # x+y+z)^2 )+n+1)), n=0 to infinity

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
