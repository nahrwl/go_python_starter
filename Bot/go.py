#!/usr/bin/env python
# Ported from the Ants starter package from aichallenge 2011
import sys
import traceback
import random
import time
from collections import defaultdict
from math import sqrt

from . import board

class Go():
    def __init__(self):
        self.initial_timebank = 0
        self.time_per_move = 10
        self.your_bot = "not set"
        self.your_botid = -1
        self.field_width = 0
        self.field_height = 0

        self.field = None
        self.round = 0
        self.turn = 0
        self.my_points = 0
        self.opponent_points = 0
        self.last_update = 0
        self.last_timebank = 0


    def update(self, data):
        'parse input'
        # start timer
        self.last_update = time.time()
        for line in data.split('\n'):
            line = line.strip().lower()
            if len(line) > 0:
                tokens = line.split()
                key0 = tokens[0]
                if key0 == "settings":
                    key1 = tokens[1]
                    if key1 == "timebank":
                        self.timebank = int(tokens[2])
                    if key1 == "time_per_move":
                        self.time_per_move = int(tokens[2])
                    if key1 == "player_names":
                        self.player_names = tokens[2].split(',')
                    if key1 == "your_bot":
                        self.your_bot = tokens[2]
                    if key1 == "your_botid":
                        self.your_botid = int(tokens[2])
                    if key1 == "field_width":
                        self.field_width = int(tokens[2])
                    if key1 == "field_height":
                        self.field_height = int(tokens[2])
                elif key0 == "update":
                    key1 = tokens[1]
                    if key1 == "game":
                        key2 = tokens[2]
                        if key2 == "round":
                            self.round = int(tokens[3])
                        elif key2 == "move":
                            self.move = int(tokens[3])
                        elif key2 == "field":
                            if self.field == None:
                                self.field = board.Board(self.your_botid, self.field_width, self.field_height)
                            self.field.parse(tokens[3])
                elif key0 == "action" and tokens[1] == "move":
                    self.last_timebank = int(tokens[2])
                    # Launching bot logic happens after setup finishes
                elif key0 == "quit":
                    pass # FIXME replace this?


#    def setup(self, data):
#        'parse initial input'
#        self.update(data)
                        
    def time_remaining(self):
        return self.last_timebank - int(1000 * (time.clock() - self.last_update))
    
    def issue_order(self, order):
        """issue an order, noting that (col, row) is the expected output
        however internally, (row, col) is used."""
        (row, col) = order
        sys.stdout.write('place_move %s %s\n' % (col, row))
        sys.stdout.flush()

    def legal_moves(self):
        legal = []
        for (ri, row) in enumerate(self.field.cell):
            for (ci, cell) in enumerate(row):
                if cell == board.EMPTY:
                    legal.append((ri, ci))
        return legal
        
    def run(self, bot):
        'parse input, update game state and call the bot classes do_turn method'
        not_finished = True
        data = ''
        while(not_finished):
            try:
                current_line = sys.stdin.readline().rstrip('\r\n') # string new line char
                data += current_line + "\n"
                if current_line.lower().startswith("action move"):
                    self.update(data)
                    if (bot.game == None):
                        bot.setup(self)
                    bot.do_turn()
                elif current_line.lower().startswith("quit"):
                    not_finished = False
            except EOFError:
                break
            except KeyboardInterrupt:
                raise
            except:
                # don't raise error or return so that bot attempts to stay alive
                traceback.print_exc(file=sys.stderr)
                sys.stderr.flush()
