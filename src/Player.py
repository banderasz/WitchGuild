from typing import List
import numpy as np
import copy

from src.Potion import Potion
from src.ResourceType import ResourceType
from src.Table import Table
from src.Tile import TileType, Tile


class Player:
    def __init__(self):
        self.actions = 5
        self.resources = {resource: 0 for resource in ResourceType}
        self.potions = list()
        self.tile = None
        self.hand_limit = 10

    def sum_resources(self):
        return sum([v for v in self.resources.values()])

    def gather(self):
        if self.tile.tile_type is TileType.TOWN:
            raise ValueError("Can't gather in town")
        gathered = self.tile.gather()
        self.actions -= 1
        if self.sum_resources() + gathered > self.hand_limit:
            gathered = self.hand_limit - self.sum_resources()
        self.resources[self.tile.get_token()] += gathered

    def move_to(self, tile: Tile):
        if self.tile:
            distance = self.tile.distance_to(tile)
            if distance > self.actions:
                raise NotEnoughAction
            self.actions -= distance
            self.tile.players.discard(self)
        self.tile = tile
        self.tile.players.add(self)

    def fulfill_order(self, potion: Potion):
        if not self.actions:
            raise NotEnoughAction
        for res_type, value in potion.resources.items():
            if self.resources[res_type] < value:
                raise NotEnoughResource
        self.actions -= 1
        for res_type, value in potion.resources.items():
            self.resources[res_type] -= value
        self.potions.append(potion)

    def sum_point(self):
        return sum([potion.point for potion in self.potions])

    def action(self, table: Table, orders: List[Potion]):
        prioritized = sorted(orders, key=self.priority_potion, reverse=True)



    def priority_potion(self, potion: Potion):
        missing = sum([value - self.resources[key] for key, value in potion.resources.items() if value > self.resources[key]])
        return np.divide(potion.point, missing)




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


class NotEnoughResource(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        print('calling str')
        if self.message:
            return 'Not enough resource, {0} '.format(self.message)
        else:
            return 'Not enough resource'

