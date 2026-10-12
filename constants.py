import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

PLAYER_SPEED = 200

DIRECTIONS = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0)
}