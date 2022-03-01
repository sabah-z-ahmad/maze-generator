import random
import time
import window
import pygame


# This function chooses valid neighbors to the provided cell in the relative
# directions according to the desired mode (NE, NW, SE, or SW). It then chooses
# at random one of the valid neighbors (if any exist) and removes the walls
# between the provided cell and the chosen neighbor
def choose_and_remove_walls(surface, g, cell, mode, animate):
    choices = []

    # Get the neighbors (if any) in the North and East directions relative
    # to the current cell
    if mode == "NE":
        c1 = cell.get_neighbor(g.grid, "North")
        c2 = cell.get_neighbor(g.grid, "East")

    # Get the neighbors (if any) in the North and West directions relative
    # to the current cell
    if mode == "NW":
        c1 = cell.get_neighbor(g.grid, "North")
        c2 = cell.get_neighbor(g.grid, "West")

    # Get the neighbors (if any) in the South and East directions relative
    # to the current cell
    if mode == "SE":
        c1 = cell.get_neighbor(g.grid, "South")
        c2 = cell.get_neighbor(g.grid, "East")

    # Get the neighbors (if any) in the South and West directions relative
    # to the current cell
    if mode == "SW":
        c1 = cell.get_neighbor(g.grid, "South")
        c2 = cell.get_neighbor(g.grid, "West")

    # Add valid neighbors to list of choices
    if c1 != None:
        choices.append(c1)
    if c2 != None:
        choices.append(c2)

    # If the list of choices contains at least one valid neighbor
    if len(choices) > 0:
        # Choose a random neighbor from the list of choices
        neighbor = choices[int(random.random() * len(choices)) - 1]

        # Remove the wall between the current cell and the chosen neighbor
        g.remove_walls_between(cell, neighbor)

    if animate:
        # Update the screen
        window.draw(surface, g.grid)

        # Delay
        time.sleep(0.05)


# Generate a maze on the grid using the binary tree algorithm.
def generate(surface, g, mode, animate):
    # Initialize a list to choose unvisited grid cells from
    unvisited_list = []
    for row in g.grid:
        for cell in row:
            unvisited_list.append(cell)

    # Loop until all grid cells have been visited
    while len(unvisited_list) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
        #
        current_cell = unvisited_list[int(random.random() * len(unvisited_list)) - 1]
        current_cell.set_visited()
        current_cell.update_unvisited_neighbors(g.grid)

        choose_and_remove_walls(surface, g, current_cell, mode, animate)

        unvisited_list.remove(current_cell)
