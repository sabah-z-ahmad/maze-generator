import pygame
import huntandkill
import growingtree
import binarytree
import grid
import solver
import window

# Screen and grid constants
WIDTH = 800
ROWS = 10
COLS = ROWS

YELLOW    = (255, 255,   0)

## Main
def main():
    surface = window.init_surface(WIDTH)
    g = grid.Grid(ROWS, COLS, WIDTH)

    start = None
    end = None

    running = True
    while running:
        window.draw(surface, g.grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Check left mouse button
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = window.get_clicked_pos(pos, WIDTH, ROWS)
                cell = g.grid[row][col]

                if not start and cell != end:
                    start = cell
                    start.set_start()

                elif not end and cell != start:
                    end = cell
                    end.set_end()

                elif cell != start and cell != end:
                    cell.color = YELLOW

            # Check right mouse button
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = window.get_clicked_pos(pos, WIDTH, ROWS)
                cell = g.grid[row][col]
                cell.reset()
                if cell == start:
                    start = None

                elif cell == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                # 'C' will reset the grid
                if event.key == pygame.K_c:
                    g = grid.Grid(ROWS, COLS, WIDTH)

                # 'H' will generate a new maze using the hunt and kill algorithm
                if event.key == pygame.K_h:
                    start = None
                    end = None
                    g = grid.Grid(ROWS, COLS, WIDTH)
                    huntandkill.generate(surface, g, True)

                # 'B' will generate a new maze using the growing tree algorithm in backtrack mode
                if event.key == pygame.K_b:
                    start = None
                    end = None
                    g = grid.Grid(ROWS, COLS, WIDTH)
                    growingtree.generate(surface, g, "Backtrack", True)

                # 'P' will generate a new maze using the growing tree algorithm in random (Prim's) mode
                if event.key == pygame.K_p:
                    start = None
                    end = None
                    g = grid.Grid(ROWS, COLS, WIDTH)
                    growingtree.generate(surface, g, "Random", True)

                # 'T' will generate a new maze using the binary tree algorithm
                # Available modes are NE, NW, SE, and SW
                if event.key == pygame.K_t:
                    start = None
                    end = None
                    g = grid.Grid(ROWS, COLS, WIDTH)
                    binarytree.generate(surface, g, "NE", True)

                # 'R' will reset the maze (remove solution)
                if event.key == pygame.K_r:
                    for row in g.grid:
                        for cell in row:
                            if cell == start:
                                cell.set_start()
                            elif cell == end:
                                cell.set_end()
                            else:
                                cell.reset()

                # Run A* algorithm to find the shortest path between start and end
                if event.key == pygame.K_SPACE and start != None and end != None:
                    for row in g.grid:
                        for cell in row:
                            cell.update_accessible_neighbors(g.grid)
                    solver.run_astar_algo(lambda: window.draw(surface, g.grid), g.grid, start, end, False)


    pygame.quit()



main()
