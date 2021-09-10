from src.ResourceType import ResourceType
from src.Tile import TileType, Tile


class Player:
    def __init__(self):
        self.actions = 5
        self.resources = {resource: 0 for resource in ResourceType}
        self.orders = set()
        self.tile = None

    def sum_resources(self):
        return sum([v for v in self.resources.values()])

    def gather(self):
        if self.tile.tile_type is TileType.TOWN:
            raise ValueError("Can't gather in town")
        gathered = self.tile.gather()
        self.actions -= 1
        if self.sum_resources() + gathered > 10:
            gathered = 10 - self.sum_resources()
        self.resources[self.tile.get_token()] += gathered

    def move_to(self, tile: Tile):
        distance = self.tile.distance_to(tile)
        if distance > self.actions:
            raise NotEnoughAction
        self.actions -= distance
        self.tile.free = True
        self.tile = tile
        self.tile.free = False


class NotEnoughAction(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        print('calling str')
        if self.message:
            return 'Not enough action, {0} '.format(self.message)
        else:
            return 'Not enough action'
