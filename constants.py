
"""Define game settings, asset paths, controls, and gameplay constants."""

import pygame
from tile import TileType
from power_up import PowerUp


# Board dimensions and screen resolution.
BOARD_ROWS = 13
BOARD_COLS = 15
TILE_SIZE = 40

SCREEN_WIDTH = BOARD_COLS * TILE_SIZE
SCREEN_HEIGHT = BOARD_ROWS * TILE_SIZE


# Player movement and collision settings.
PLAYER_SPEED = 200
PLAYER_SIZE = 30
PLAYER_MOVE_MARGIN = 12


# Tiles that must remain empty around player spawn positions.
SPAWN_CLEAR_TILES = {
    (1,1),
    (1,2),
    (2,1),
    (11, 13),
    (11, 12),
    (10, 13),
}


# Explosion dimensions and timing.
EXPLOSION_SIZE = 40
EXPANSION_INTERVAL = 0.05
EXPLOSION_HOLD_TIME = 0.3


# Image paths for power-ups.
POWERUP_IMAGES = {
    PowerUp.BOMB_UP: "assets/images/power_ups/bomb_up.png",
    PowerUp.FIRE_UP: "assets/images/power_ups/fire_up.png",
    PowerUp.SPEED_UP: "assets/images/power_ups/speed_up.png",
}


# Image path for bombs.
BOMB_IMAGE = "assets/images/bombs/bomb.png"


# Image paths for explosion sprites.
EXPLOSION_IMAGES = {
    "center": "assets/images/explosions/center.png",
    "horizontal": "assets/images/explosions/horizontal.png",
    "vertical": "assets/images/explosions/vertical.png",
}


# Image paths for board tiles.
TILE_IMAGES = {
    TileType.EMPTY: "assets/images/tiles/empty.png",
    TileType.DESTRUCTIBLE: "assets/images/tiles/destructible.png",
    TileType.WALL:"assets/images/tiles/wall.png",
}


# Image paths for player one sprites.
PLAYER1_IMAGES = {
    "UP": "assets/images/players/player1_up.png",
    "RIGHT": "assets/images/players/player1_right.png",
    "LEFT": "assets/images/players/player1_left.png",
    "DOWN": "assets/images/players/player1_down.png",
    "END" : "assets/images/players/player1_end.png",
}


# Image paths for player two sprites.
PLAYER2_IMAGES = {
    "UP": "assets/images/players/player2_up.png",
    "RIGHT": "assets/images/players/player2_right.png",
    "LEFT": "assets/images/players/player2_left.png",
    "DOWN": "assets/images/players/player2_down.png",
    "END" : "assets/images/players/player2_end.png",
}


# Number of power-ups randomly placed under destructible walls.
BOMB_UP_COUNT = 5
FIRE_UP_COUNT = 5
SPEED_UP_COUNT = 4


# Player speed settings and speed power-up increment.
SPEED_UP_INCREMENT = 40
INITIAL_PLAYER_SPPED = 200
MAX_PLAYER_SPEED = 400


# Keyboard controls for player one.
DIRECTIONS_P1 = {
    pygame.K_UP: "UP",
    pygame.K_DOWN: "DOWN",
    pygame.K_LEFT: "LEFT",
    pygame.K_RIGHT: "RIGHT"
}


# Keyboard controls for player two.
DIRECTIONS_P2 = {
    pygame.K_w: "UP",
    pygame.K_s: "DOWN",
    pygame.K_a: "LEFT",
    pygame.K_d: "RIGHT"
}


# Movement vectors for each direction (dx, dy).
DIRECTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0)
}


# Directions in which explosions propagate.
EXPLOSION_DIRECTIONS = [
    (0, -1),
    (0, 1),
    (-1, 0),
    (1, 0)
]
