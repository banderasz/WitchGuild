from typing import List

from src.Player import Player
from src.Potion import Potion
from src.Table import Table


class Game:
    def __init__(self, number_of_players):
        self.number_of_players = number_of_players
        self.players: List[Player] = []
        self.table = Table()
        self.orders: List[Potion] = []
        self.init_game()

    def init_game(self):
        for _ in range(self.number_of_players):
            player = Player()
            player.move_to(self.table.get_center())
            self.players.append(player)
        for _ in range(self.number_of_players - 1):
            self.orders.append(Potion.get_random_order())

    def start_game(self):
        self.round()

    def round(self):
        for player in self.players:
            player.actions = 5
            self.turn(player)



    def turn(self, player: Player):
        player.action(self.table, self.orders)
