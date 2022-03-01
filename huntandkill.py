import window
import random
import time
import pygame


## Maze generation functions
#
def walk(surface, g, current_cell, animate):
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

        # Set the current cell to be the new cell
        current_cell = new_cell

        if animate:
            # Update the screen
            window.draw(surface, g.grid)

            # Delay
            time.sleep(0.05)


#
def hunt(surface, g, animate):
    for row in g.grid:
        for cell in row:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    
            # If cell is not visited
            if not cell.is_visited():
                cell.update_visited_neighbors(g.grid)
                # But cell has at least one visited neighbor
                if len(cell.visited_neighbors) > 0:
                    # Set cell as visited
                    cell.set_visited()
                    cell.update_unvisited_neighbors(g.grid)

                    # Choose a random visited neighbor to connect cell to
                    rand_visited_cell = cell.visited_neighbors[int(random.random() * len(cell.visited_neighbors)) - 1]

                    # Remove walls between cell and the randomly chosen visited neighbor
                    g.remove_walls_between(cell, rand_visited_cell)

                    if animate:
                        # Update the screen
                        window.draw(surface, g.grid)

                        # Delay
                        time.sleep(0.05)

                    return cell

    return None



#
def generate(surface, g, animate):
    start_row = int(random.random() * g.rows)
    start_col = int(random.random() * g.cols)

    current_cell = g.grid[start_row][start_col]
    current_cell.set_visited()
    current_cell.update_unvisited_neighbors(g.grid)

    while current_cell != None:
        #
        walk(surface, g, current_cell, animate)

        #
        current_cell = hunt(surface, g, animate)
