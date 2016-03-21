import random

class Bot:


    def __init__(self):
        self.game = None

    def setup(self, game):
        self.game = game

    def do_turn(self):
        legal = self.game.legal_moves()
        chosen = random.choice(legal)
        self.game.issue_order(chosen)

