
import random
from typing import TYPE_CHECKING  # Used for type hints without causing circular imports

import pygame

from tile import TileType
from power_up import PowerUp
from constants import (
    BOARD_COLS,
    BOARD_ROWS,
    TILE_SIZE,
    PLAYER_SIZE,
    SPAWN_CLEAR_TILES,
    BOMB_UP_COUNT,
    FIRE_UP_COUNT,
    SPEED_UP_COUNT
)

# Import Explosion only for type annotations.
# TYPE_CHECKING is True for type checkers (like Pylance),
# but False at runtime, preventing circular imports.
if TYPE_CHECKING:
    from explosion import Explosion


class Board():
    """Represent the game board, including walls, collisions, and power-ups."""

    def __init__(self) -> None:
        """Initialize the board and generate hidden power-ups."""
        self.board = self._generate_board()
        self.power_ups = self._generate_powerups()

    def draw(self, screen: pygame.Surface, surfaces: dict[TileType, pygame.Surface]) -> None:
        """Draw the board using the corresponding sprite for each tile.

        Args:
            screen: Pygame surface on which to draw the board.
            surfaces: Dictionary mapping tile types to their sprites.
        """
        for row, tiles in enumerate(self.board):
            for column, tile in enumerate(tiles):
                screen.blit(surfaces[tile], (column * TILE_SIZE, row * TILE_SIZE))

    def _generate_board(self) -> list[list[TileType]]:
        """Generate the board with fixed walls, destructible walls, and clear spawn areas."""
        board = []
        for row_index in range(BOARD_ROWS):
            row = []
            for column_index in range(BOARD_COLS):
                if row_index == 0 or row_index == BOARD_ROWS - 1 or column_index == 0 or column_index == BOARD_COLS - 1:
                    row.append(TileType.WALL)
                elif not row_index % 2 and not column_index % 2:
                    row.append(TileType.WALL)
                elif (row_index,column_index) in SPAWN_CLEAR_TILES:
                    row.append(TileType.EMPTY)
                else:
                    row.append(TileType.DESTRUCTIBLE)
            board.append(row)
        return board

    def _get_destructible_walls(self) -> list[tuple[int, int]]:
        """Return the coordinates of all destructible walls as (col, row) tuples."""
        return [
            (column, row)
            for row, tiles in enumerate(self.board)
            for column, tile in enumerate(tiles)
            if tile == TileType.DESTRUCTIBLE]

    def _generate_powerups(self) -> dict[tuple[int, int], PowerUp]:
        """Randomly assign power-ups to destructible wall tiles."""
        destructible_walls = self._get_destructible_walls()
        power_ups_quantity = BOMB_UP_COUNT + FIRE_UP_COUNT + SPEED_UP_COUNT
        chosen_tiles = random.sample(destructible_walls, power_ups_quantity)
        power_ups = {}
        for tile in chosen_tiles[0:BOMB_UP_COUNT]:
            power_ups[tile] = PowerUp.BOMB_UP
        for tile in chosen_tiles[BOMB_UP_COUNT : BOMB_UP_COUNT + FIRE_UP_COUNT]:
            power_ups[tile] = PowerUp.FIRE_UP
        for tile in chosen_tiles[BOMB_UP_COUNT + FIRE_UP_COUNT :]:
            power_ups[tile] = PowerUp.SPEED_UP
        return power_ups


    def print_board(self) -> None:
        """Print a text representation of the board for debugging."""
        for row in self.board:
            for column in row:
                print(column.value, end="")
            print()

    def _is_horizontal_rail(self, y: float) -> int:
        """Return the row parity used to identify horizontal movement corridors.

        Args:
            y: Player's Y position in pixels.

        Returns:
            int: 1 for odd rows and 0 for even rows.
        """
        center = y + PLAYER_SIZE / 2
        row = center // TILE_SIZE
        return row % 2

    def _is_vertical_rail(self, x: float) -> int:
        """Return the column parity used to identify vertical movement corridors.

        Args:
            x: Player's X position in pixels.

        Returns:
            int: 1 for odd columns and 0 for even columns.
        """
        center = x + PLAYER_SIZE / 2
        col = center // TILE_SIZE
        return col % 2

    def _is_inside(self, row: int, col: int) -> bool:
        """Check whether the specified row and column are inside the board.

        Args:
            row: Row index.
            col: Column index.

        Returns:
            bool: True if the coordinates are inside the board.
        """
        if row < 0 or row >= BOARD_ROWS or col < 0 or col >= BOARD_COLS:
            return False
        return True

    def _is_walkable(self, row: int, col: int) -> bool:
        """Check whether a tile is inside the board and empty.

        Args:
            row: Row index.
            col: Column index.

        Returns:
            bool: True if the tile can be walked on.
        """
        if self._is_inside(row, col):
            return self.board[row][col] == TileType.EMPTY
        return False

    def can_occupy(self, x: float, y: float, width: float, height: float) -> bool:
        """Check whether a rectangle can occupy a position without hitting walls.

        Args:
            x: Rectangle's X position in pixels.
            y: Rectangle's Y position in pixels.
            width: Rectangle width in pixels.
            height: Rectangle height in pixels.

        Returns:
            bool: True if all occupied tiles are walkable.
        """
        occupied_cols = []
        occupied_rows = []
        occupied_cols.append(int(x//TILE_SIZE))
        occupied_cols.append(int(((x + width) - 0.000001) // TILE_SIZE))
        occupied_rows.append(int(y//TILE_SIZE))
        occupied_rows.append(int(((y + height) - 0.000001) // TILE_SIZE))
        for row in occupied_rows:
            for col in occupied_cols:
                if not self._is_walkable(row, col):
                    return False
        return True

    def destroy_tiles(self, affected_tiles: list[tuple[int, int]]) -> None:
        """Replace destructible walls with empty tiles after an explosion.

        Args:
            affected_tiles: Tiles reached by the explosion.
        """
        for tile in affected_tiles:
            if self.board[tile[1]][tile[0]] == TileType.DESTRUCTIBLE:
                self.board[tile[1]][tile[0]] = TileType.EMPTY

    def _has_fire(self, tile: tuple[int, int], explosions: list["Explosion"]) -> bool:
        """Check whether a tile is currently affected by an active explosion.

        Args:
            tile: Tile coordinates as (col, row).
            explosions: Currently active explosions.

        Returns:
            bool: True if the tile contains active fire.
        """
        return any(tile in explosion.active_tiles for explosion in explosions)

    def draw_powerups(self, screen: pygame.Surface, explosions: list["Explosion"], surfaces: dict[PowerUp, pygame.Surface]) -> None:
        """Draw exposed power-ups that are not covered by active explosions.

        Args:
            screen: Pygame surface on which to draw power-ups.
            explosions: Currently active explosions.
            surfaces: Dictionary mapping power-up types to their sprites.
        """
        for tile, power_up in self.power_ups.items():
            if self.board[tile[1]][tile[0]] == TileType.EMPTY and not self._has_fire(tile, explosions):
                screen.blit(surfaces[power_up], (tile[0] * TILE_SIZE, tile[1] * TILE_SIZE))

    def collect_powerup(self, tile: tuple[int, int], explosions: list["Explosion"]) -> PowerUp | None:
        """Collect an exposed power-up if the tile is not affected by fire.

        Args:
            tile: Tile coordinates occupied by the player.
            explosions: Currently active explosions.

        Returns:
            PowerUp | None: Collected power-up, or None if unavailable.
        """
        if tile in self.power_ups:
            if self.board[tile[1]][tile[0]] == TileType.EMPTY and not self._has_fire(tile, explosions):
                return self.power_ups.pop(tile)
        return None

    def destroy_powerups(self, tiles: list[tuple[int, int]]) -> None:
        """Destroy exposed power-ups in newly affected explosion tiles.

        Args:
            tiles: Tiles newly reached by an explosion.
        """
        for tile in tiles:
            if tile in self.power_ups:
                if self.board[tile[1]][tile[0]] == TileType.EMPTY:
                    del self.power_ups[tile]
