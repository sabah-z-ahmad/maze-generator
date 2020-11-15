import pygame
import math
from queue import PriorityQueue

## Solver
# Heuristic for h-score
def heuristic(p1, p2):
    # Unpack tuple
    x1, y1 = p1
    x2, y2, = p2

    # Manhatten distance
    return abs((x1 - x2) + (y1 - y2))


# Follow the the came from chain backwards from the end position to the start position
def reconstruct_path(came_from, current, draw, animate):
    while current in came_from:
        current = came_from[current]
        current.set_path()
        if animate:
            draw()

    if animate:
        draw()


# A* Algorithm
def run_astar_algo(draw, grid, start, end, animate):
    # Tie-breaker
    count = 0

    # Initialize a priority queue for the open set
    open_set = PriorityQueue()

    # Add the starting cell to the open set
    open_set.put((0, count, start))

    # Dictionary to record the cell just before any given cell was reached
    came_from = {}

    # Dictionary of g-scores
    g_score = {cell: float("inf") for row in grid for cell in row}
    g_score[start] = 0

    # Dictionary of f-scores
    f_score = {cell: float("inf") for row in grid for cell in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    # Used to search the open_set as a priority queue cannot be searched.
    # Must be synhcronized with open_set
    open_set_hash = {start}

    # Continue until no cells remain in the open set
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw, animate)
            end.set_end()
            start.set_start()
            return True

        # Consider all neighbors of current Node
        for neighbor in current.accessible_neighbors:
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

        # Draw each step to screen if desired
        if animate:
            draw()

        # Place the current cell into the closed set
        if current != start:
            current.set_closed()

    return False


##########################################33
