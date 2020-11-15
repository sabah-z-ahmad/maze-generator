import pygame

# Color constants
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
BLUE      = (  0,   0, 255)
YELLOW    = (255, 255,   0)
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
PURPLE    = (128,   0, 128)
ORANGE    = (255, 165,   0)
GREY      = (128, 128, 128)
TURQUOISE = ( 64, 224, 208)


VISITED_CELL_COLOR   = WHITE
UNVISITED_CELL_COLOR = GREY
START_CELL_COLOR     = BLUE
END_CELL_COLOR       = ORANGE
WALL_COLOR           = BLACK


## Cell class
class Cell:
    def __init__(self, row, col, width, total_rows, total_cols):
        self.row = row
        self.col = col
        self.width = width / total_rows
        self.height = width / total_cols
        self.total_rows = total_rows
        self.total_cols = total_cols

        self.x = col * self.width
        self.y = row * self.height

        self.walls = {"North":True, "South":True, "West":True, "East":True}

        self.accessible_neighbors = []
        self.unvisited_neighbors = []
        self.visited_neighbors = []

        self.color = UNVISITED_CELL_COLOR
        self.visited = False

    def get_pos(self):
        return self.row, self.col

    def is_visited(self):
        return self.visited

    def set_visited(self):
        self.visited = True
        self.color = VISITED_CELL_COLOR

    def set_start(self):
        self.color = START_CELL_COLOR

    def set_end(self):
        self.color = END_CELL_COLOR

    def set_closed(self):
        self.color = RED

    def set_open(self):
        self.color = GREEN

    def set_path(self):
        self.color = PURPLE

    def reset(self):
        if self.visited:
            self.color = VISITED_CELL_COLOR
        else:
            self.color = UNVISITED_CELL_COLOR

    def draw(self, surface):
        wall_size = 3
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

        # Upper Wall
        if self.walls["North"]:
            pygame.draw.line(surface, WALL_COLOR, [self.x, self.y], [self.x + self.width, self.y], wall_size)

        # Lower Wall
        if self.walls["South"]:
            pygame.draw.line(surface, WALL_COLOR, [self.x, self.y + self.height], [self.x + self.width, self.y + self.height], wall_size)

        # Left Wall
        if self.walls["West"]:
            pygame.draw.line(surface, WALL_COLOR, [self.x, self.y], [self.x, self.y + self.height], wall_size)

        # Right Wall
        if self.walls["East"]:
            pygame.draw.line(surface, WALL_COLOR, [self.x + self.width, self.y], [self.x + self.width, self.y + self.height], wall_size)

    def update_accessible_neighbors(self, grid):
        self.accessible_neighbors = []

        # Check for an accessible neighbor in the DOWN direction
        if self.row < self.total_rows - 1 and not self.walls["South"]:
            self.accessible_neighbors.append(grid[self.row + 1][self.col])

        # Check for an accessible neighbor in the UP direction
        if self.row > 0 and not self.walls["North"]:
            self.accessible_neighbors.append(grid[self.row - 1][self.col])

        # Check for an accessible neighbor in the LEFT direction
        if self.col > 0 and not self.walls["West"]:
            self.accessible_neighbors.append(grid[self.row][self.col - 1])

        # Check for an accessible neighbor in the RIGHT direction
        if self.col < self.total_cols - 1 and not self.walls["East"]:
            self.accessible_neighbors.append(grid[self.row][self.col + 1])

    def update_unvisited_neighbors(self, grid):
        self.unvisited_neighbors = []

        # Check for an unvisited neighbor in the DOWN direction
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_visited():
            self.unvisited_neighbors.append(grid[self.row + 1][self.col])

        # Check for an unvisited neighbor in the UP direction
        if self.row > 0 and not grid[self.row - 1][self.col].is_visited():
            self.unvisited_neighbors.append(grid[self.row - 1][self.col])

        # Check for an unvisited neighbor in the LEFT direction
        if self.col > 0 and not grid[self.row][self.col - 1].is_visited():
            self.unvisited_neighbors.append(grid[self.row][self.col - 1])

        # Check for an unvisited neighbor in the RIGHT direction
        if self.col < self.total_cols - 1 and not grid[self.row][self.col + 1].is_visited():
            self.unvisited_neighbors.append(grid[self.row][self.col + 1])

    def update_visited_neighbors(self, grid):
        self.visited_neighbors = []

        # Check for a visited neighbor in the DOWN direction
        if self.row < self.total_rows - 1 and grid[self.row + 1][self.col].is_visited():
            self.visited_neighbors.append(grid[self.row + 1][self.col])

        # Check for a visited neighbor in the UP direction
        if self.row > 0 and grid[self.row - 1][self.col].is_visited():
            self.visited_neighbors.append(grid[self.row - 1][self.col])

        # Check for a visited neighbor in the LEFT direction
        if self.col > 0 and grid[self.row][self.col - 1].is_visited():
            self.visited_neighbors.append(grid[self.row][self.col - 1])

        # Check for a visited neighbor in the RIGHT direction
        if self.col < self.total_cols - 1 and grid[self.row][self.col + 1].is_visited():
            self.visited_neighbors.append(grid[self.row][self.col + 1])

    # Remove a single wall (Top, Bottom, Left, or Right)
    def remove_wall(self, wall):
        self.walls[wall] = False

    # Return the neighbor in a given direction relative to self. If no such
    # neighbor exists, return None
    def get_neighbor(self, grid, direction):
        if direction == "North":
            if self.row > 0:
                return grid[self.row - 1][self.col]

        elif direction == "South":
            if self.row < self.total_rows - 1:
                return grid[self.row + 1][self.col]

        elif direction == "West":
            if self.col > 0:
                return grid[self.row][self.col - 1]

        elif direction == "East":
            if self.col < self.total_cols - 1:
                return grid[self.row][self.col + 1]

        return None
