from enum import Enum

class GameState(Enum):
    PLAYING = "playing"
    RESOLVING = "resolving"
    GAME_OVER = "game_over"
