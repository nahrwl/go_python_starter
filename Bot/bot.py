import Random

class Bot:


    def __init__(self):
        self.game = None

    def setup(self, game):
        self.game = game

    def do_turn(self):
        legal = self.game.legal_moves()
        chosen = Random.choice(legal)
        return chosen

