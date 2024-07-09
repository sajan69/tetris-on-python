import pygame
import random
import json
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Define shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1], [1, 1]]
]

# Game variables
grid = [[0] * (SCREEN_WIDTH // BLOCK_SIZE) for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
current_shape = random.choice(SHAPES)
current_shape_pos = [0, (SCREEN_WIDTH // BLOCK_SIZE) // 2 - len(current_shape[0]) // 2]
score = 0
high_scores_file = "high_scores.json"

# Load high scores
if os.path.exists(high_scores_file):
    with open(high_scores_file, 'r') as f:
        high_scores = json.load(f)
else:
    high_scores = []

def save_high_score(score):
    global high_scores
    high_scores.append(score)
    high_scores = sorted(high_scores, reverse=True)[:5]
    with open(high_scores_file, 'w') as f:
        json.dump(high_scores, f)

def draw_grid():
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            color = RED if grid[y][x] else GRAY
            pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def draw_shape(shape, position):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, WHITE, ((position[1] + x) * BLOCK_SIZE, (position[0] + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def rotate_shape(shape):
    return [list(reversed(col)) for col in zip(*shape)]

def can_move(shape, position):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                new_x = position[1] + x
                new_y = position[0] + y
                if new_x < 0 or new_x >= len(grid[0]) or new_y >= len(grid) or grid[new_y][new_x]:
                    return False
    return True

def merge_shape_to_grid(shape, position):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                grid[position[0] + y][position[1] + x] = 1

def clear_lines():
    global grid, score
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    cleared_lines = len(grid) - len(new_grid)
    score += cleared_lines * 10  # Increment score by 10 for each cleared line
    new_grid = [[0] * len(grid[0]) for _ in range(cleared_lines)] + new_grid
    grid = new_grid

def draw_text(text, size, color, position):
    font = pygame.font.Font(None, size)
    surface = font.render(text, True, color)
    screen.blit(surface, position)

def opening_screen():
    screen.fill(BLACK)
    draw_text("TETRIS", 50, WHITE, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 100))
    draw_text("Press P to Play", 30, WHITE, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2))
    draw_text("Press H for High Scores", 30, WHITE, (SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 + 40))
    draw_text("Press A for About", 30, WHITE, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 80))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    waiting = False
                elif event.key == pygame.K_h:
                    high_scores_screen()
                    waiting = False
                elif event.key == pygame.K_a:
                    about_screen()
                    waiting = False

def game_over_screen():
    global score
    screen.fill(BLACK)
    draw_text("GAME OVER", 50, WHITE, (SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 - 100))
    draw_text(f"Score: {score}", 30, WHITE, (SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2))
    draw_text("Press any key to play again", 30, WHITE, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50))
    pygame.display.flip()
    waiting = True
    save_high_score(score)
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def high_scores_screen():
    screen.fill(BLACK)
    draw_text("HIGH SCORES", 50, WHITE, (SCREEN_WIDTH // 2 - 120, 50))
    for i, score in enumerate(high_scores):
        draw_text(f"{i+1}. {score}", 30, WHITE, (SCREEN_WIDTH // 2 - 50, 100 + i * 40))
    draw_text("Press any key to return", 30, WHITE, (SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT - 50))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False
    opening_screen()

def about_screen():
    screen.fill(BLACK)
    draw_text("ABOUT", 50, WHITE, (SCREEN_WIDTH // 2 - 60, 50))
    draw_text("Tetris game implemented using ", 30, WHITE, (20, 150))
    draw_text("Python and Pygame.", 30, WHITE, (20, 190))
    draw_text("Author: Sajan Adhikari", 30, WHITE, (20, 230))
    draw_text("Press any key to return", 30, WHITE, (SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT - 50))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False
    opening_screen()

def main():
    global current_shape, current_shape_pos, score, grid
    clock = pygame.time.Clock()
    running = True

    opening_screen()

    while running:
        screen.fill(BLACK)
        draw_grid()
        draw_shape(current_shape, current_shape_pos)
        draw_text(f"Score: {score}", 36, WHITE, (10, 10))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    new_pos = [current_shape_pos[0], current_shape_pos[1] - 1]
                    if can_move(current_shape, new_pos):
                        current_shape_pos = new_pos
                elif event.key == pygame.K_RIGHT:
                    new_pos = [current_shape_pos[0], current_shape_pos[1] + 1]
                    if can_move(current_shape, new_pos):
                        current_shape_pos = new_pos
                elif event.key == pygame.K_DOWN:
                    new_pos = [current_shape_pos[0] + 1, current_shape_pos[1]]
                    if can_move(current_shape, new_pos):
                        current_shape_pos = new_pos
                elif event.key == pygame.K_UP:
                    new_shape = rotate_shape(current_shape)
                    if can_move(new_shape, current_shape_pos):
                        current_shape = new_shape

        if not can_move(current_shape, [current_shape_pos[0] + 1, current_shape_pos[1]]):
            merge_shape_to_grid(current_shape, current_shape_pos)
            clear_lines()
            current_shape = random.choice(SHAPES)
            current_shape_pos = [0, (SCREEN_WIDTH // BLOCK_SIZE) // 2 - len(current_shape[0]) // 2]
            if not can_move(current_shape, current_shape_pos):
                game_over_screen()
                score = 0
                grid = [[0] * (SCREEN_WIDTH // BLOCK_SIZE) for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
                current_shape = random.choice(SHAPES)
                current_shape_pos = [0, (SCREEN_WIDTH // BLOCK_SIZE) // 2 - len(current_shape[0]) // 2]
        else:
            current_shape_pos[0] += 1

        clock.tick(10)
    pygame.quit()

if __name__ == "__main__":
    main()
