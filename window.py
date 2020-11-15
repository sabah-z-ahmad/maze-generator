import pygame

# Color constants
CLEAR_COLOR = (255, 255, 255)


# Initialize a square pygame surface
def init_surface(width):
    surface = pygame.display.set_mode((width + 1, width + 1))
    return surface


# Draw the grid to the surface
def draw(surface, grid):
    surface.fill(CLEAR_COLOR)

    for row in grid:
        for cell in row:
            cell.draw(surface)

    pygame.display.update()


# Find the [row, column] corresponsing to the position clicked on the screen
def get_clicked_pos(pos, width, rows):
    x, y = pos
    cell_width = width / rows
    row = int(y / cell_width)
    col = int(x / cell_width)

    return row, col
