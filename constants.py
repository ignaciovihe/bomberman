import pygame
from tile import TileType
from power_up import PowerUp

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

PLAYER_SPEED = 200
PLAYER_SIZE = 30
PLAYER_MOVE_MARGIN = 12
PLAYER_COLOR = {
    1: "blue",
    2: "green"
}

BOARD_ROWS = 13
BOARD_COLS = 15
SPAWN_CLEAR_TILES = {
    (1,1),
    (1,2),
    (2,1),
    (11, 13),
    (11, 12),
    (10, 13),
}

BOMB_RADIUS = 15

EXPLOSION_SIZE = 40
EXPANSION_INTERVAL = 0.05
EXPLOSION_HOLD_TIME = 0.3

POWERUP_IMAGES = {
    PowerUp.BOMB_UP: "assets/images/power_ups/bomb_up.png",
    PowerUp.FIRE_UP: "assets/images/power_ups/fire_up.png",
    PowerUp.SPEED_UP: "assets/images/power_ups/speed_up.png",
}
BOMB_IMAGE = "assets/images/bombs/bomb.png"

EXPLOSION_IMAGES = {
    "center": "assets/images/explosions/center.png",
    "horizontal": "assets/images/explosions/horizontal.png",
    "vertical": "assets/images/explosions/vertical.png",
}

BOMB_UP_COUNT = 5
FIRE_UP_COUNT = 5
SPEED_UP_COUNT = 4

SPEED_UP_INCREMENT = 40
INITIAL_PLAYER_SPPED = 200
MAX_PLAYER_SPEED = 400

TILE_COLORS = {
    TileType.EMPTY: "grey",
    TileType.WALL : "black",
    TileType.DESTRUCTIBLE : "brown",
}

TILE_SIZE = 40

DIRECTIONS_P1 = {
    pygame.K_UP: "UP",
    pygame.K_DOWN: "DOWN",
    pygame.K_LEFT: "LEFT",
    pygame.K_RIGHT: "RIGHT"
}

DIRECTIONS_P2 = {
    pygame.K_w: "UP",
    pygame.K_s: "DOWN",
    pygame.K_a: "LEFT",
    pygame.K_d: "RIGHT"
}

DIRECTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0) 
}


EXPLOSION_DIRECTIONS = [
    (0, -1),
    (0, 1),
    (-1, 0),
    (1, 0)
]