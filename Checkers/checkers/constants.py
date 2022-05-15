import pygame

# Window size
WIDTH, HEIGHT = 1280, 700

ROWS, COLS = 8, 8

SQUARE_SIZE = (HEIGHT//ROWS)

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
CYAN = (0, 255, 255)

# Crown asset
CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))

# Background asset
BG = pygame.image.load("assets/Background.png")