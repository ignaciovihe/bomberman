
from constants import PLAYER_SIZE, TILE_SIZE, EXPLOSION_DIRECTIONS
from board import Board
from tile import TileType
import pygame


class Bomb():
    """Represent a bomb with a countdown timer and explosion range."""

    def __init__(self, x: float, y: float, id_player: int, power: int) -> None:
        """Initialize a bomb with its position, owner, and explosion power.

        Args:
            x: Player's X position when placing the bomb.
            y: Player's Y position when placing the bomb.
            id_player: ID of the player who placed the bomb.
            power: Maximum explosion range in tiles.
        """
        self.x = x
        self.y = y
        self.tile = self._calculate_tile()
        self.center = self._calculate_tile_center()
        self.id_player = id_player
        self.timer = 3.0
        self.owner_can_pass = True
        self.power = power

    def _calculate_tile(self) -> tuple[int, int]:
        """Calculate the tile (col, row) containing the player's center."""
        player_center_x = self.x + PLAYER_SIZE / 2
        player_center_y = self.y + PLAYER_SIZE / 2
        bomb_tile_x = int(player_center_x // TILE_SIZE)
        bomb_tile_y = int(player_center_y // TILE_SIZE)
        return (bomb_tile_x, bomb_tile_y)

    def _calculate_tile_center(self) -> tuple[float, float]:
        """Calculate the center position of the bomb's tile in pixels."""
        bomb_x = (self.tile[0] * TILE_SIZE) + TILE_SIZE / 2
        bomb_y = (self.tile[1] * TILE_SIZE) + TILE_SIZE / 2
        return (bomb_x, bomb_y)

    def overlaps_player(self, x: float, y: float) -> bool:
        """Check whether the bomb overlaps a player's collision rectangle.

        Args:
            x: Player's X position in pixels.
            y: Player's Y position in pixels.

        Returns:
            bool: True if the bomb overlaps the player.
        """
        bomb_rect = pygame.Rect(
            self.tile[0] * TILE_SIZE,
            self.tile[1] * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE
        )

        player_rect = pygame.Rect(
            x,
            y,
            PLAYER_SIZE,
            PLAYER_SIZE
        )

        return bomb_rect.colliderect(player_rect)

    def check_explosions(self, board: Board) -> list[tuple[int, int]]:
        """Calculate the tiles affected by the bomb's explosion.

        The explosion spreads in four directions, stops at solid walls,
        and includes destructible walls before stopping.

        Args:
            board: Game board used to check obstacles.

        Returns:
            list[tuple[int, int]]: Affected tiles as (col, row) coordinates.
        """
        affected_tiles = [self.tile]
        for direction in EXPLOSION_DIRECTIONS:
            dx, dy = direction
            for distance in range(1, self.power +1):
                tile_affected_x = self.tile[0] + dx * distance
                tile_affected_y = self.tile[1] + dy * distance
                if not board._is_inside(tile_affected_y, tile_affected_x):
                    break
                if board.board[tile_affected_y][tile_affected_x] == TileType.WALL:
                    break
                if board.board[tile_affected_y][tile_affected_x] == TileType.DESTRUCTIBLE:
                    affected_tiles.append((tile_affected_x,tile_affected_y))
                    break
                if board.board[tile_affected_y][tile_affected_x] == TileType.EMPTY:
                    affected_tiles.append((tile_affected_x,tile_affected_y))
        return affected_tiles

    def update(self, dt: float) -> None:
        """Decrease the bomb's countdown timer.

        Args:
            dt: Time elapsed since the previous frame in seconds.
        """
        self.timer -= dt

    def draw(self, screen: pygame.Surface, surface: pygame.Surface) -> None:
        """Draw the bomb sprite at its tile position.

        Args:
            screen: Pygame surface on which to draw the bomb.
            surface: Image surface representing the bomb.
        """
        screen.blit(surface, (self.tile[0] * TILE_SIZE, self.tile[1] * TILE_SIZE))
