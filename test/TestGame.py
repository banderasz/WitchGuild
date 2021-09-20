import unittest

from src.Game import Game
from src.ResourceType import ResourceType


class TestGame(unittest.TestCase):

    def setUp(self) -> None:
        self.game = Game(15)

    def test_game(self):
        self.game.players[0].resources[ResourceType.HERB] += 10
        self.game.players[0].resources[ResourceType.CRYSTAL] += 10
        self.game.start_game()