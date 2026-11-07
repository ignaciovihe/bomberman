
from enum import Enum


class GameState(Enum):
    """Represent the different states of the game."""

    MENU = "menu"
    PLAYING = "playing"
    RESOLVING = "resolving"
    GAME_OVER = "game_over"

