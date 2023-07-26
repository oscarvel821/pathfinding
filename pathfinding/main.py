import pygame
from pygame.locals import *
from grid import Grid
 
SCREEN_HEIGHT = 1280
SCREEN_WIDTH = 1420

def draw_text(text, font, text_col,screen, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def main():

    pygame.init()

    #define font
    font = pygame.font.SysFont(None, 20)

    #bfs grid variables
    bfs_grid_width = 35
    bfs_grid_height = 35
    bfs_surface_width = SCREEN_WIDTH // 2
    bfs_surface_height = SCREEN_HEIGHT // 2
    bfs_width_size = bfs_surface_width // bfs_grid_width
    bfs_height_size = bfs_surface_height // bfs_grid_height
    bfs_prev_cell = None
    bfs_prev_cell_idx = None
    bfs_start_cell_idx = None
    bfs_end_cell_idx = None
    bfs_finished = False

    #dfs grid variables
    dfs_grid_width = 35
    dfs_grid_height = 35
    dfs_surface_width = SCREEN_WIDTH // 2
    dfs_surface_height = SCREEN_HEIGHT // 2
    dfs_width_size = dfs_surface_width // dfs_grid_width
    dfs_height_size = dfs_surface_height // dfs_grid_height
    dfs_prev_cell = None
    dfs_prev_cell_idx = None
    dfs_start_cell_idx = None
    dfs_finished = False

    #astar grid variables
    astar_grid_width = 35
    astar_grid_height = 35
    astar_surface_width = SCREEN_WIDTH // 2
    astar_surface_height = SCREEN_HEIGHT // 2
    astar_width_size = astar_surface_width // astar_grid_width
    astar_height_size = astar_surface_height // astar_grid_height
    astar_prev_cell = None
    astar_prev_cell_idx = None
    astat_start_cell_idx = None
    astar_finished = False

    #grids
    bfs_grid = Grid(bfs_grid_width, bfs_grid_height, bfs_surface_width, bfs_surface_height, bfs_width_size, bfs_height_size, 10, 10, bfs_algo=True)
    dfs_grid = Grid(dfs_grid_width, dfs_grid_height, dfs_surface_width, dfs_surface_height, dfs_width_size, dfs_height_size, bfs_surface_width + 5, 10, dfs_algo=True)
    astar_grid = Grid(astar_grid_width, astar_grid_height, astar_surface_width, astar_surface_height, astar_width_size, astar_height_size, 10, astar_surface_height + 5, aStar_algo=True)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Path Finding")

    clock = pygame.time.Clock()

    running = 1

    #animation variables
    mouse_pressed = False
    s_key_pressed = False
    e_key_pressed = False
    pause = True

    while running:
        # Clear the screen
        screen.fill((0, 0, 0))

        #draw the map
        bfs_grid.drawGrid(screen, font)
        dfs_grid.drawGrid(screen, font)
        astar_grid.drawGrid(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 0
                pygame.quit()
                quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pressed = False
                bfs_prev_cell = None
                dfs_prev_cell = None
                astar_prev_cell = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = not pause
                elif event.key == pygame.K_r:
                    pause = True
                    bfs_finished = False
                    dfs_finished = False
                    astar_finished = False
                    bfs_grid.resetGrid()
                    dfs_grid.resetGrid()
                    astar_grid.resetGrid()
                elif event.key == pygame.K_a:
                    pause = True
                    bfs_finished = False
                    dfs_finished = False
                    astar_finished = False
                    bfs_grid.resetAnimation()
                    dfs_grid.resetAnimation()
                    astar_grid.resetAnimation()
                elif event.key == pygame.K_s:
                    pause = True
                    s_key_pressed = True
                elif event.key == pygame.K_e:
                    pause = True
                    e_key_pressed = True
            if event.type == pygame.KEYUP:
                s_key_pressed = False
                e_key_pressed = False

        if mouse_pressed:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if s_key_pressed:
                pause = True
                valid, bfs_start_cell_idx = bfs_grid.moveStartCell((mouse_x, mouse_y))
                if valid:
                    dfs_grid.setStartCell(bfs_start_cell_idx)
                    astar_grid.setStartCell(bfs_start_cell_idx)
                    bfs_finished = False
                    dfs_finished = False
                    astar_finished = False
                # if bfs_grid.moveStartCell((mouse_x, mouse_y)):
                #     dfs_grid.resetAnimation()
                #     astar_grid.resetAnimation()
                #     bfs_finished = False
                #     dfs_finished = False
                #     astar_finished = False
                # elif dfs_grid.moveStartCell((mouse_x, mouse_y)):
                #     bfs_grid.resetAnimation()
                #     astar_grid.resetAnimation()
                #     bfs_finished = False
                #     dfs_finished = False
                #     astar_finished = False
                # elif astar_grid.moveStartCell((mouse_x, mouse_y)):
                #     bfs_grid.resetAnimation()
                #     dfs_grid.resetAnimation()
                #     bfs_finished = False
                #     dfs_finished = False
                #     astar_finished = False
                # bfs_finished = False
                # dfs_finished = False
            elif e_key_pressed:
                pause = True
                valid, bfs_end_cell_idx = bfs_grid.moveEndCell((mouse_x, mouse_y))
                if valid:
                    dfs_grid.setEndCell(bfs_end_cell_idx)
                    astar_grid.setEndCell(bfs_end_cell_idx)
                    bfs_finished = False
                    dfs_finished = False
                    astar_finished = False
                # bfs_grid.moveEndCell((mouse_x, mouse_y))
                # dfs_grid.moveEndCell((mouse_x, mouse_y))
                # bfs_finished = False
                # dfs_finished = False
            else:
                bfs_prev_cell, bfs_prev_cell_idx = bfs_grid.toggle_wall((mouse_x, mouse_y), bfs_prev_cell)
                dfs_grid.setWall(bfs_prev_cell_idx)
                astar_grid.setWall(bfs_prev_cell_idx)
                # dfs_prev_cell = dfs_grid.toggle_wall((mouse_x, mouse_y), dfs_prev_cell)

        if not pause:
            if not bfs_finished:
                bfs_finished = bfs_grid.solveMap()
            if not dfs_finished:
                dfs_finished = dfs_grid.solveMap()
            if not astar_finished:
                astar_finished = astar_grid.solveMap()

        pygame.display.update()

        # Limit the framerate
        clock.tick(60)

if __name__ == "__main__":
    main()