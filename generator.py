import random
import pygame
import math
from queue import PriorityQueue

WIDTH = 990
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Maze Generator With Pathfinding")

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

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    # Is this node in the closed set
    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def is_unvisited(self):
        return self.color == YELLOW

    def is_empty(self):
        return self.color == WHITE

    def reset(self):
        self.color = WHITE

    def set_closed(self):
        self.color = RED

    def set_open(self):
        self.color = GREEN

    def set_barrier(self):
        self.color = BLACK

    def set_start(self):
        self.color = ORANGE

    def set_end(self):
        self.color = TURQUOISE

    def set_path(self):
        self.color = PURPLE

    def set_unvisited(self):
        self.color = YELLOW

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []     # ????not needed?????

        # Check for valid neighbor in DOWN direction
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        # Check for valid neighbor in UP direction
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        # Check for valid neighbor in RIGHT direction
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        # Check for valid neighbor in LEFT direction
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def heuristic(p1, p2):
    # Unpack tuple
    x1, y1 = p1
    x2, y2, = p2

    # Manhatten ('L') distance
    return abs((x1 - x2) + (y1 - y2))


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.set_path()
        draw()


def run_astar_algo(draw, grid, start, end):
    count = 0       # Used to break ties

    open_set = PriorityQueue()
    open_set.put((0, count, start))

    came_from = {}

    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    # Used to search the open_set, must be synhcronized with open_set
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.set_end()
            start.set_start()
            return True

        # Consider all neighbors of current Node
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            # If a shorter path to the neighbor is found
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.set_open()

        draw()

        if current != start:
            current.set_closed()

    return False


def build_grid(rows, width):
    grid = []
    gap = width / rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid


def draw_grid(win, rows, width):
    gap = width / rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def num_neighbors(rand_wall, grid):
    n = 0
    if grid[rand_wall[0] - 1][rand_wall[1]].is_empty():
        n += 1
    if grid[rand_wall[0] + 1][rand_wall[1]].is_empty():
        n += 1
    if grid[rand_wall[0]][rand_wall[1] - 1].is_empty():
        n += 1
    if grid[rand_wall[0]][rand_wall[1] + 1].is_empty():
        n += 1

    return n


def generate_maze(ROWS, grid):
    for row in grid:
        for node in row:
            node.set_unvisited()

    starting_height = int(random.random() * ROWS)
    starting_width = int(random.random() * ROWS)

    if starting_height == 0:
        starting_height += 1
    if starting_height == ROWS - 1:
        starting_height -= 1

    if starting_width == 0:
        starting_width += 1
    if starting_width == ROWS - 1:
        starting_width -= 1

    grid[starting_height][starting_width].reset()
    walls = []
    walls.append([starting_height - 1, starting_width])
    walls.append([starting_height, starting_width - 1])
    walls.append([starting_height, starting_width + 1])
    walls.append([starting_height + 1, starting_width])

    grid[starting_height - 1][starting_width].set_barrier()
    grid[starting_height][starting_width - 1].set_barrier()
    grid[starting_height][starting_width + 1].set_barrier()
    grid[starting_height + 1][starting_width].set_barrier()

    while walls:
        # Choose a random wall
        rand_wall = walls[int(random.random() * len(walls)) - 1]

        # Check the left wall
        if rand_wall[1] != 0:
            if grid[rand_wall[0]][rand_wall[1] - 1].is_unvisited() and grid[rand_wall[0]][rand_wall[1] + 1].is_empty():
                # Find the number of non-wall neighbors
                n = num_neighbors(rand_wall, grid)

                if n < 2:
                    # Set the cell as non-wall
                    grid[rand_wall[0]][rand_wall[1]].reset()

                    # Set the new walls
                    # Upper node
                    if rand_wall[0] != 0:
                        if not grid[rand_wall[0] - 1][rand_wall[1]].is_empty():
                            grid[rand_wall[0] - 1][rand_wall[1]].set_barrier()
                        if [rand_wall[0] - 1, rand_wall[1]] not in walls:
                            walls.append([rand_wall[0] - 1, rand_wall[1]])

                    # Lower node
                    if rand_wall[0] != ROWS - 1:
                        if not grid[rand_wall[0] + 1][rand_wall[1]].is_empty():
                            grid[rand_wall[0] + 1][rand_wall[1]].set_barrier()
                        if [rand_wall[0] + 1, rand_wall[1]] not in walls:
                            walls.append([rand_wall[0] + 1, rand_wall[1]])

                    # Left node
                    if rand_wall[1] != 0:
                        if not grid[rand_wall[0]][rand_wall[1] - 1].is_empty():
                            grid[rand_wall[0]][rand_wall[1] - 1].set_barrier()
                        if [rand_wall[0], rand_wall[1] - 1] not in walls:
                            walls.append([rand_wall[0], rand_wall[1] - 1])

                # Delete walls
                for wall in walls:
                    if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                        walls.remove(wall)

                continue

        # Check the upper wall
        if rand_wall[0] != 0:
            if grid[rand_wall[0] - 1][rand_wall[1]].is_unvisited() and grid[rand_wall[0] + 1][rand_wall[1]].is_empty():
                # Find the number of non-wall neighbors
                n = num_neighbors(rand_wall, grid)

                if n < 2:
                    # Set the cell as non-wall
                    grid[rand_wall[0]][rand_wall[1]].reset()

                    # Set the new walls
                    # Upper node
                    if rand_wall[0] != 0:
                        if not grid[rand_wall[0] - 1][rand_wall[1]].is_empty():
                            grid[rand_wall[0] - 1][rand_wall[1]].set_barrier()
                        if [rand_wall[0] - 1, rand_wall[1]] not in walls:
                            walls.append([rand_wall[0] - 1, rand_wall[1]])

                    # Left node
                    if rand_wall[1] != 0:
                        if not grid[rand_wall[0]][rand_wall[1] - 1].is_empty():
                            grid[rand_wall[0]][rand_wall[1] - 1].set_barrier()
                        if [rand_wall[0], rand_wall[1] - 1] not in walls:
                            walls.append([rand_wall[0], rand_wall[1] - 1])

                    # Right node
                    if rand_wall[1] != ROWS - 1:
                        if not grid[rand_wall[0]][rand_wall[1] + 1].is_empty():
                            grid[rand_wall[0]][rand_wall[1] + 1].set_barrier()
                        if [rand_wall[0], rand_wall[1] + 1] not in walls:
                            walls.append([rand_wall[0], rand_wall[1] + 1])

                # Delete walls
                for wall in walls:
                    if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                        walls.remove(wall)

                continue

        # Check the lower wall
        if rand_wall[0] != ROWS - 1:
            if grid[rand_wall[0] + 1][rand_wall[1]].is_unvisited() and grid[rand_wall[0] - 1][rand_wall[1]].is_empty():
                # Find the number of non-wall neighbors
                n = num_neighbors(rand_wall, grid)

                if n < 2:
                    # Set the cell as non-wall
                    grid[rand_wall[0]][rand_wall[1]].reset()

                    # Set the new walls
                    # Lower node
                    if rand_wall[0] != 0:
                        if not grid[rand_wall[0] + 1][rand_wall[1]].is_empty():
                            grid[rand_wall[0] + 1][rand_wall[1]].set_barrier()
                        if [rand_wall[0] + 1, rand_wall[1]] not in walls:
                            walls.append([rand_wall[0] + 1, rand_wall[1]])

                    # Left node
                    if rand_wall[1] != 0:
                        if not grid[rand_wall[0]][rand_wall[1] - 1].is_empty():
                            grid[rand_wall[0]][rand_wall[1] - 1].set_barrier()
                        if [rand_wall[0], rand_wall[1] - 1] not in walls:
                            walls.append([rand_wall[0], rand_wall[1] - 1])

                    # Right node
                    if rand_wall[1] != ROWS - 1:
                        if not grid[rand_wall[0]][rand_wall[1] + 1].is_empty():
                            grid[rand_wall[0]][rand_wall[1] + 1].set_barrier()
                        if [rand_wall[0], rand_wall[1] + 1] not in walls:
                            walls.append([rand_wall[0], rand_wall[1] + 1])

                # Delete walls
                for wall in walls:
                    if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                        walls.remove(wall)

                continue

        # Check the right wall
        if rand_wall[1] != ROWS - 1:
            if grid[rand_wall[0]][rand_wall[1] + 1].is_unvisited() and grid[rand_wall[0]][rand_wall[1] - 1].is_empty():
                # Find the number of non-wall neighbors
                n = num_neighbors(rand_wall, grid)

                if n < 2:
                    # Set the cell as non-wall
                    grid[rand_wall[0]][rand_wall[1]].reset()

                    # Set the new walls
                    # Upper node
                    if rand_wall[0] != 0:
                        if not grid[rand_wall[0] - 1][rand_wall[1]].is_empty():
                            grid[rand_wall[0] - 1][rand_wall[1]].set_barrier()
                        if [rand_wall[0] - 1, rand_wall[1]] not in walls:
                            walls.append([rand_wall[0] - 1, rand_wall[1]])

                    # Lower node
                    if rand_wall[0] != ROWS - 1:
                        if not grid[rand_wall[0] + 1][rand_wall[1]].is_empty():
                            grid[rand_wall[0] + 1][rand_wall[1]].set_barrier()
                        if [rand_wall[0] + 1, rand_wall[1]] not in walls:
                            walls.append([rand_wall[0] + 1, rand_wall[1]])

                    # Right node
                    if rand_wall[1] != 0:
                        if not grid[rand_wall[0]][rand_wall[1] + 1].is_empty():
                            grid[rand_wall[0]][rand_wall[1] + 1].set_barrier()
                        if [rand_wall[0], rand_wall[1] + 1] not in walls:
                            walls.append([rand_wall[0], rand_wall[1] + 1])

                # Delete walls
                for wall in walls:
                    if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                        walls.remove(wall)

                continue

        # Delete the wall from the list anyways
        for wall in walls:
            if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                walls.remove(wall)

    # Set the remaining unvisited nodes as walls
    for row in grid:
        for node in row:
            if node.is_unvisited():
                node.set_barrier()

    # Set start (entrance) and end (exit)
    start = None
    end = None
    for i in range(0,ROWS):
        if grid[1][i].is_empty():
            start = grid[0][i]
            start.set_start()
            break

    for i in range(ROWS - 1, 0, -1):
        if grid[ROWS - 2][i].is_empty():
            end = grid[ROWS - 1][i]
            end.set_end()
            break

    return start, end


def get_clicked_pos(pos, rows, width):
    gap = width / rows
    y, x = pos
    row = int(y / gap)
    col = int(x / gap)

    return row, col


def main(win, width):
    ROWS = 99
    grid = build_grid(ROWS, width)

    start = None
    end = None

    running = True

    while running:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Check left mouse button
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]

                if not start and node != end:
                    start = node
                    start.set_start()

                elif not end and node != start:
                    end = node
                    end.set_end()

                elif node != start and node != end:
                    node.set_barrier()

            # Check right mouse button
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None

                if node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    run_astar_algo(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = build_grid(ROWS, width)

                if event.key == pygame.K_g:
                    start, end = generate_maze(ROWS, grid)


    pygame.quit()


main(WIN, WIDTH)
