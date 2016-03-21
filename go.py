#!/usr/bin/env python
import sys
import traceback
import random
import time
from collections import defaultdict
from math import sqrt

EMPTY, FRIEND, ENEMY, LIBERTY, KO = range(0, 5)

AIM = {'n': (-1, 0),
       'e': (0, 1),
       's': (1, 0),
       'w': (0, -1)}

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
                                self.field = Board(field.width, field.height)
                            self.field.parse(tokens[3])
                elif key0 == "action" and tokens[1] == "move":
                    self.last_timebank = int(tokens[2])
                    # Launching bot logic happens after setup finishes
                elif key0 == "quit":
                    pass # FIXME replace this?


    def setup(self, data):
        'parse initial input'
        self.update(data)
                        
    def time_remaining(self):
        return self.last_timebank - int(1000 * (time.clock() - self.last_update))
    
    def issue_order(self, order):
        'issue an order'
        (row, col) = order
        sys.stdout.write('place_move %s %s\n' % (row, col))
        sys.stdout.flush()
        
    def run(bot):
        'parse input, update game state and call the bot classes do_turn method'
        ants = Ants()
        map_data = ''
        while(True):
            try:
                current_line = sys.stdin.readline().rstrip('\r\n') # string new line char
                if current_line.lower() == 'ready':
                    ants.setup(map_data)
                    bot.do_setup(ants)
                    ants.finish_turn()
                    map_data = ''
                elif current_line.lower() == 'go':
                    ants.update(map_data)
                    # call the do_turn method of the class passed in
                    bot.do_turn(ants)
                    ants.finish_turn()
                    map_data = ''
                else:
                    map_data += current_line + '\n'
            except EOFError:
                break
            except KeyboardInterrupt:
                raise
            except:
                # don't raise error or return so that bot attempts to stay alive
                traceback.print_exc(file=sys.stderr)
                sys.stderr.flush()
