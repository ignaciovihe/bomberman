import pygame
from tile import TileType

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

PLAYER_SPEED = 200
PLAYER_SIZE = 30
PLAYER_MOVE_MARGIN = 12

BOARD_ROWS = 13
BOARD_COLS = 15

TILE_COLORS = {
    TileType.EMPTY: "grey",
    TileType.WALL : "black",
    TileType.DESTRUCTIBLE : "brown",
}

TILE_SIZE = 40

DIRECTIONS = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0)
}