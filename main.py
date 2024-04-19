# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 16:04:43 2024

@author: Mosco

This is a simple implementation of Tetris using Pygame. It includes basic gameplay elements
like moving and rotating tetrominos, scoring, and clearing lines. The game runs until the
tetrominoes stack to the top of the screen, at which point a 'Game Over' message is displayed.
"""

import pygame
import random

# Constants defining screen dimensions and tile size
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
TILE_SIZE = 30
GAME_WIDTH, GAME_HEIGHT = SCREEN_WIDTH // TILE_SIZE, SCREEN_HEIGHT // TILE_SIZE

# Color definitions
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)  # Color for locked Tetrominos
BLACK = (0, 0, 0)   # Text color

# Tetromino shapes formatted to include all rotations
SHAPES = [
    # Each list within SHAPES corresponds to a Tetromino type and its rotations
    # I shape
    [
        [[1], [1], [1], [1]],  # Vertical
        [[1, 1, 1, 1]]         # Horizontal
    ],
    # O shape
    [
        [[1, 1], 
         [1, 1]]
    ],
    # S shape
    [
        [[0, 1, 1], 
         [1, 1, 0]],
        [[1, 0],
         [1, 1],
         [0, 1]]
    ],
    # Z shape
    [
        [[1, 1, 0],
         [0, 1, 1]],
        [[0, 1],
         [1, 1],
         [1, 0]]
    ],
    # T shape
    [
        [[0, 1, 0],
         [1, 1, 1]],
        [[1, 0],
         [1, 1],
         [1, 0]],
        [[1, 1, 1],
         [0, 1, 0]],
        [[0, 1],
         [1, 1],
         [0, 1]]
    ]
]

pygame.init()  # Initialize all imported pygame modules
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetris')

# Game variables
clock = pygame.time.Clock()
fall_time = 0
fall_speed = 0.8  # Seconds between automatic drops
game_grid = [[0] * GAME_WIDTH for _ in range(GAME_HEIGHT)]
score = 0
font = pygame.font.Font(None, 48)  # Default font and size

def draw_grid():
    """
    Draws the grid on which the Tetrominos fall. Empty spaces are gray and occupied spaces are blue.
    """
    for i in range(GAME_HEIGHT):
        for j in range(GAME_WIDTH):
            rect = pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            color = BLUE if game_grid[i][j] else GRAY
            pygame.draw.rect(screen, color, rect, 0 if game_grid[i][j] else 1)

def draw_score():
    """
    Displays the current score in the top-left corner of the screen.
    """
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (5, 5))

def clear_lines():
    """
    Checks for complete lines in the grid, clears them, moves everything above down,
    and increases the score. Returns True if any lines were cleared.
    """
    global score
    need_to_clear = []
    for i, row in enumerate(game_grid):
        if all(row):
            need_to_clear.append(i)
    for i in need_to_clear:
        del game_grid[i]
        game_grid.insert(0, [0] * GAME_WIDTH)
        score += 10
    return len(need_to_clear) > 0

class Tetromino:
    """
    Represents a Tetromino piece with methods for drawing, moving, rotating,
    and checking collisions.
    """
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice([(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 120, 0)])
        self.rotation = 0

    def draw(self):
        """
        Draws the Tetromino on the screen according to its current position and rotation.
        """
        for i, row in enumerate(self.shape[self.rotation % len(self.shape)]):
            for j, cell in enumerate(row):
                if cell == 1:
                    pygame.draw.rect(
                        screen, 
                        self.color,
                        (self.x + j * TILE_SIZE, self.y + i * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                        0
                    )

    def move(self, dx, dy):
        """
        Attempts to move the Tetromino by dx, dy. Returns True if movement was successful, False if blocked.
        """
        new_x = self.x + dx
        new_y = self.y + dy
        if not self.check_collision(new_x, new_y, self.rotation):
            self.x = new_x
            self.y = new_y
            return False
        return True

    def rotate(self):
        """
        Rotates the Tetromino to the next rotation state. Rotation is skipped if it would cause a collision.
        """
        new_rotation = (self.rotation + 1) % len(self.shape)
        if not self.check_collision(self.x, self.y, new_rotation):
            self.rotation = new_rotation

    def check_collision(self, x, y, rotation):
        """
        Checks for collisions between the Tetromino and the edges of the game area or other locked Tetrominos.
        Returns True if a collision is detected.
        """
        for i, row in enumerate(self.shape[rotation % len(self.shape)]):
            for j, cell in enumerate(row):
                if cell == 1:
                    grid_x = (x // TILE_SIZE) + j
                    grid_y = (y // TILE_SIZE) + i
                    if grid_x >= GAME_WIDTH or grid_x < 0 or grid_y >= GAME_HEIGHT or game_grid[grid_y][grid_x]:
                        return True
        return False

    def lock(self):
        """
        Locks the Tetromino in place on the grid when it can no longer move down.
        """
        for i, row in enumerate(self.shape[self.rotation % len(self.shape)]):
            for j, cell in enumerate(row):
                if cell == 1:
                    grid_x = (self.x // TILE_SIZE) + j
                    grid_y = (self.y // TILE_SIZE) + i
                    game_grid[grid_y][grid_x] = 1  # Mark the grid as occupied

def get_new_tetromino():
    """
    Generates a new random Tetromino.
    """
    return Tetromino(SCREEN_WIDTH // 2 - TILE_SIZE * 2, 0, random.choice(SHAPES))

def draw_game_over():
    """
    Displays the 'Game Over' message at the center of the screen.
    """
    game_over_text = font.render("Game Over!", True, (255, 0, 0))
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

def main():
    """
    Main game loop. Manages game state updates, drawing, and user input.
    """
    global fall_speed
    running = True
    game_over = False
    current_piece = get_new_tetromino()
    last_time = pygame.time.get_ticks()
    
    while running:
        screen.fill(WHITE)
        draw_grid()
        current_piece.draw()
        draw_score()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.move(-TILE_SIZE, 0)
                elif event.key == pygame.K_RIGHT:
                    current_piece.move(TILE_SIZE, 0)
                elif event.key == pygame.K_DOWN:
                    current_piece.move(0, TILE_SIZE)
                elif event.key == pygame.K_UP:
                    current_piece.rotate()

        current_time = pygame.time.get_ticks()
        if (current_time - last_time) > (fall_speed * 1000):
            last_time = current_time
            if current_piece.move(0, TILE_SIZE):
                current_piece.lock()
                clear_lines()
                current_piece = get_new_tetromino()
                if current_piece.check_collision(current_piece.x, current_piece.y, current_piece.rotation):
                    game_over = True
                if game_over:
                    draw_game_over()
                    pygame.display.update()
                    pygame.time.wait(2000)
                    running = False
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
