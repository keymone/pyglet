class Point:
    def __init__(self, pos, col):
        if len(pos) == 2:
            pos = [*pos, 0, 1]
        elif len(pos) == 3:
            pos = [*pos, 1]

        if len(col) == 3:
            col = [*col, 1]

        self.pos = pos
        self.col = col
