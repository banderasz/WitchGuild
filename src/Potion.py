import random
from enum import Enum

from src.ResourceType import ResourceType


class Potion(Enum):
    EyeColorChanging = (1, 1, 1, 0, 0, 0)
    Rejuvenating = (2, 0, 2, 1, 1, 0)
    Love = (3, 2, 1, 1, 0, 2)
    Wart = (1, 0, 0, 0, 1, 1)
    Dulling = (2, 1, 1, 0, 2, 0)
    FrogTransformer = (3, 1, 0, 2, 1, 2)
    AntiHangover = (1, 0, 1, 0, 1, 0)
    ShapeShifting = (2, 1, 1, 0, 1, 1)
    Truth = (3, 1, 1, 2, 1, 1)
    Growth = (1, 1, 0, 0, 0, 1)
    Invisibility = (2, 1, 0, 2, 1, 0)
    Health = (3, 1, 2, 1, 1, 1)

    def __init__(self, point, crystal=0, herb=0, mushroom=0, spider_web=0, bat_wing=0):
        self.point = point
        self.resources = {ResourceType.CRYSTAL: crystal, ResourceType.HERB: herb, ResourceType.MUSHROOM: mushroom,
                          ResourceType.SPIDER_WEB: spider_web, ResourceType.BAT_WING: bat_wing}

    @staticmethod
    def get_random_order():
        return random.choice(list(Potion))
