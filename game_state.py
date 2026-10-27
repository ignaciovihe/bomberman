from enum import Enum

class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    RESOLVING = "resolving"
    GAME_OVER = "game_over"
