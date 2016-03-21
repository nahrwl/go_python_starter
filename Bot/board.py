
EMPTY, FRIEND, ENEMY, LIBERTY, KO = range(0, 5)

ADJACENT = (
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1)
)

class Board:
    def __init__(self, friend_id, width, height):
        self.friend_id = friend_id
        self.width = width
        self.height = height
        self.cell = [[EMPTY for col in range (0, width)] for row in range(0, height)]

    def int_to_cell(self, i):
        if i == 0:
            return EMPTY
    #    elif i == 3:
    #        return KO
        elif i == self.friend_id:
            return FRIEND
        else:
            return ENEMY

    def parse(self, data):
        cells = data.split(',')
        col = 0
        row = 0
        for cell in cells:
            if (col >= self.width):
                col = 0
                row +=1
            self.cell[row][col] = self.int_to_cell(int(cell))
            col += 1
