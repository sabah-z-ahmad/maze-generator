import pygame
import huntandkill
import grid
import solver
import window

# Screen and grid constants
WIDTH = 800
ROWS = 80
COLS = ROWS


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
                    g = grid.Grid(ROWS, COLS)

                # 'H' will generate a new maze using the hunt and kill algorithm
                if event.key == pygame.K_h:
                    start = None
                    end = None
                    g = grid.Grid(ROWS, COLS, WIDTH)
                    huntandkill.generate(surface, g, False)

                # Reset maze
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
                if event.key == pygame.K_SPACE:
                    for row in g.grid:
                        for cell in row:
                            cell.update_accessible_neighbors(g.grid)
                    solver.run_astar_algo(lambda: window.draw(surface, g.grid), g.grid, start, end, False)


    pygame.quit()



main()
