import random
import time
from math import sqrt

import pygame

INF = float('inf')

# Initialize Pygame
pygame.init()

# Set up the game window
pygame.display.set_caption("Pygame go brrr")
white = (255,255,255)
black = (0, 0, 0)
red = (255, 0, 0)
pixel_size = 35
maze_size = 19
screen = pygame.display.set_mode((maze_size * pixel_size, maze_size * pixel_size))
font = pygame.font.SysFont("timesnewroman", (int)(pixel_size / 2))

# the red robot
robot_size = 2
circle_center = (1 * pixel_size + pixel_size / 2, 1 * pixel_size + pixel_size / 2)
radius = pixel_size / 5

# boolean
is_path_found = False

# making maze
def generate_maze_dfs(n):

    number_of_white = 0

    def carve(x, y):
        nonlocal number_of_white
        maze[x][y] = 0
        number_of_white = number_of_white + 1
        directions = [(0,1), (1,0), (0,-1), (-1,0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx*2, y + dy*2
            if 0 <= nx < n and 0 <= ny < n and maze[nx][ny] == 1:
                maze[x + dx][y + dy] = 0
                number_of_white = number_of_white + 1
                carve(nx, ny)

    if n % 2 == 0:
        n += 1
    maze = [[1 for _ in range(n)] for _ in range(n)]
    carve(1,1)

    # --- break some wall ------------------------------

    number_of_black = (maze_size-2)*(maze_size-2) - number_of_white
    num_openings = max((int)(number_of_black - (maze_size-2)*(maze_size-2) / 4),0)
    opened = 0
    while opened < num_openings:
        x = random.randint(1, n - 2)
        y = random.randint(1, n - 2)
        if maze[x][y] == 1:
            maze[x][y] = 0
            opened += 1
    # -------------------------------------------------

    return maze


grid = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
[1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
[1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
[1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1],
[1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
[1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
[1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
[1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
[1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
grid = generate_maze_dfs(maze_size)


path_grid = [[INF for _ in range(maze_size)] for _ in range(maze_size)]
for i in range(maze_size):
    for j in range(maze_size):
        if grid[i][j] == 1:
            path_grid[i][j] = 0

def draw_line_between_cells(cell1, cell2, color=(0, 0, 255), width=3):
    x1, y1 = cell1
    x2, y2 = cell2

    start_pos = (x1 * pixel_size + pixel_size // 2, y1 * pixel_size + pixel_size // 2)
    end_pos = (x2 * pixel_size + pixel_size // 2, y2 * pixel_size + pixel_size // 2)

    pygame.draw.line(screen, color, start_pos, end_pos, width)

def draw():
    for x_pos in range(len(grid)):
        for y_pos in range(len(grid)):
            if grid[x_pos][y_pos] == 1:
                rectangle = pygame.Rect(x_pos*pixel_size, y_pos*pixel_size, pixel_size, pixel_size)
                pygame.draw.rect(screen, black, rectangle)
    pygame.display.update()

def mouse_draw(mouse_pos, color):
    x_pos = (int)(mouse_pos[0] / pixel_size)
    y_pos = (int)(mouse_pos[1] / pixel_size)
    rectangle = pygame.Rect(x_pos * pixel_size, y_pos * pixel_size, pixel_size, pixel_size)
    pygame.draw.rect(screen, color, rectangle)
    if color == black:
        grid[x_pos][y_pos] = 1
    else:
        if color == white:
            grid[x_pos][y_pos] = 0
    pygame.display.update()

def distance(position1, position2):
    x1, y1 = position1
    x2, y2 = position2

    return sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))

# Relaxed Dijkstra Algorithm
# 1) L(x) = 0, the obstacle node set is O;
# 2) All nodes and x ≠ s, L(x) = ∞;
# 3) Insert s point into the end of Q queue;
# 4) When Q is not empty, get the team head node v of Q;
# 5) For all four nodes x, x ∉ Q and x ∉ O adjacent to v, find L(x) = L(V) + 1, insert x into the end of queue Q, and return 4).

# Find from final to start
# 1) v = e;
# 2) When v ≠ s, find all the eight adjacent nodes x of v;
# 3) Compare 8 nodes L(x), get the smallest node x and store x;
# 4) v = x, returns 2).

def rdj(grid, robot_position, end_position):
    global path_grid
    path_length = 0

    path_grid = [[INF for _ in range(maze_size)] for _ in range(maze_size)]
    for i in range(maze_size):
        for j in range(maze_size):
            if grid[i][j] == 1:
                path_grid[i][j] = 0


    x1 = robot_position[0]
    y1 = robot_position[1]
    x2 = end_position[0]
    y2 = end_position[1]

    path_grid[x1][y1] = 0

    queue = []

    queue.append((x1,y1))
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while queue:
        current = queue.pop(0)
        x = current[0]
        y = current[1]
        if x == x2 and y == y2:
            break;
        for dx,dy in directions:
            nx, ny = x + dx, y + dy
            if path_grid[nx][ny] == INF:
                queue.append((nx,ny))
                path_grid[nx][ny] = path_grid[x][y] + 1


    # It's time for search back

    current = end_position
    path.append(current)
    if path_grid[current[0]][current[1]] == INF:
        pygame.display.update()
        return

    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),          (0, 1),
                  (1, -1), (1, 0), (1, 1)]

    min_nx, min_ny = INF, INF
    while current != robot_position:
        x, y = current
        Min = INF
        random.shuffle(directions)
        for dx,dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < maze_size - 1 and 0 < ny < maze_size  -1 and grid[nx][ny] == 0:
                if abs(nx - x) == 1 and abs(ny - y) == 1:
                    if grid[x][ny] == 1 and grid[nx][y] == 1:
                        continue
                if Min == path_grid[nx][ny]:
                    min_nx, min_ny = nx,ny
                if Min > path_grid[nx][ny]:
                    min_nx, min_ny = nx, ny
                    Min = path_grid[nx][ny]

        current = (min_nx, min_ny)
        path.append(current)
        path_length += distance((x,y),current)


    pygame.display.update()

    return path_length


robot_position = (1,1)
target = (maze_size-2, maze_size-2)
def wait_for_left_click_local(main_screen):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return event.pos
        pygame.display.flip()

def add_new_start_and_end():
    global robot_position, target

    value_text = font.render("Choose Start", True, (255, 0, 0))  # màu đỏ
    screen.blit(value_text, (5, 5))

    clicked_pos = wait_for_left_click_local(screen)

    if clicked_pos is not None:
        x_pos = (int)(clicked_pos[0] / pixel_size)
        y_pos = (int)(clicked_pos[1] / pixel_size)
        robot_position = (x_pos, y_pos)

    draw()
    pygame.display.update()

    value_text = font.render("Choose End", True, (255, 0, 0))  # màu đỏ
    screen.blit(value_text, (5, 5))

    clicked_pos = wait_for_left_click_local(screen)

    if clicked_pos is not None:
        x_pos = (int)(clicked_pos[0] / pixel_size)
        y_pos = (int)(clicked_pos[1] / pixel_size)
        target = (x_pos, y_pos)

    draw()
    pygame.display.update()

    print(robot_position, "  ", target)

# make the robot move (look fun)
def robot_moving():
    pass


# Game loop
running = True
# pygame.draw.circle(screen, red, circle_center, radius)
screen.fill(white)
draw()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Draw by hand
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_draw(event.pos, black)
                screen.fill(white)
                draw()

            if event.button == 3:
                mouse_draw(event.pos, white)
                screen.fill(white)
                draw()

        if event.type == pygame.KEYDOWN:
            if event.key == 32:

                path = []

                screen.fill(white)
                draw()

                start_time = time.perf_counter()
                print(rdj(grid, robot_position, target))
                end_time = time.perf_counter()
                print(f"Thời gian chạy rdj(): {(end_time - start_time):.6f} giây")

                for x in range(maze_size):
                    for y in range(maze_size):
                        if grid[x][y] == 0 and path_grid[x][y] != INF:
                            value_text = font.render(str(path_grid[x][y]), True, (255, 0, 0))  # màu đỏ
                            screen.blit(value_text, (x * pixel_size + pixel_size / 5, y * pixel_size + pixel_size / 5))


                while len(path) > 1:
                    cell1 = path[0]
                    cell2 = path[1]
                    path.remove(cell1)
                    draw_line_between_cells(cell1, cell2)

                path.remove(path[0])
                pygame.display.update()

        if event.type == pygame.KEYDOWN:
            if event.key == 8:
                screen.fill(white)
                draw()
                add_new_start_and_end()



# Quit Pygame
pygame.quit()