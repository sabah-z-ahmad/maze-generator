import cell

# Grid class
class Grid:
    # Initialize a blank grid
    def __init__(self, rows, cols, width):
        self.rows = rows
        self.cols = cols
        self.grid = []
        for i in range(self.rows):
            self.grid.append([])
            for j in range(self.cols):
                c = cell.Cell(i, j, width, rows, cols)
                self.grid[i].append(c)

    # Remove the walls joining two cells
    def remove_walls_between(self, c1, c2):
        if c1.row < c2.row:
            # c1 is above c2
            c1.remove_wall("South")
            c2.remove_wall("North")

        elif c1.row > c2.row:
            # c1 is below c2
            c1.remove_wall("North")
            c2.remove_wall("South")

        elif c1.col < c2.col:
            # c1 is to the left of c2
            c1.remove_wall("East")
            c2.remove_wall("West")

        elif c1.col > c2.col:
            # c1 is to the right of c2
            c1.remove_wall("West")
            c2.remove_wall("East")
