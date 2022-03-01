import random
import time
import window
import pygame


## Maze generation functions
#
def walk(surface, g, current_cell, visited_list, animate):
    # Loop until the current cell has no unvisited neighbors
    while len(current_cell.unvisited_neighbors) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
        # Choose a random unvisited neighbor as a new cell
        new_cell = current_cell.unvisited_neighbors[int(random.random() * len(current_cell.unvisited_neighbors)) - 1]

        # Remove the walls between current_cell and new_cell
        g.remove_walls_between(current_cell, new_cell)

        # Set the new cell as visited and update the new cell's list of unvisited neighbors
        new_cell.set_visited()
        new_cell.update_unvisited_neighbors(g.grid)

        # Add the new cell to the visited list
        visited_list.append(new_cell)

        # Set the current cell to be the new cell
        current_cell = new_cell

        if animate:
            # Update the screen
            window.draw(surface, g.grid)

            # Delay
            time.sleep(0.05)


#
def choose_visited_cell(g, visited_list, mode):
    if mode == "Backtrack":
        while len(visited_list) > 0:
            last = len(visited_list) - 1
            visited_list[last].update_unvisited_neighbors(g.grid)
            if len(visited_list[last].unvisited_neighbors) > 0:
                return visited_list[last]
            else:
                visited_list.remove(visited_list[last])

        return None
    elif mode == "Random":
        while len(visited_list) > 0:
            random_cell = visited_list[int(random.random() * len(visited_list)) - 1]
            random_cell.update_unvisited_neighbors(g.grid)
            if len(random_cell.unvisited_neighbors) > 0:
                return random_cell
            else:
                visited_list.remove(random_cell)

        return None


#
def generate(surface, g, mode, animate):
    start_row = int(random.random() * g.rows)
    start_col = int(random.random() * g.cols)

    current_cell = g.grid[start_row][start_col]
    current_cell.set_visited()
    current_cell.update_unvisited_neighbors(g.grid)

    visited_list = []
    visited_list.append(current_cell)

    while len(visited_list) > 0:
        #
        walk(surface, g, current_cell, visited_list, animate)

        #
        current_cell = choose_visited_cell(g, visited_list, mode)
