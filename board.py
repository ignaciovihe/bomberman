import random
from typing import TYPE_CHECKING # Used for type hints without causing circular imports

import pygame

from tile import TileType
from power_up import PowerUp
from constants import (
    BOARD_COLS, 
    BOARD_ROWS, 
    TILE_COLORS, 
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

    def __init__(self):
        self.board = self._generate_board()
        self.power_ups = self._generate_powerups()

    def draw(self, screen):
        for row_index, row in enumerate(self.board):
            for column_index, tile in enumerate(row):
                pygame.draw.rect(
                    screen, 
                    TILE_COLORS[tile],
                    (
                        column_index * TILE_SIZE,
                        row_index * TILE_SIZE, 
                        TILE_SIZE, 
                        TILE_SIZE)
                    )


    def _generate_board(self):
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

    def _get_destructible_walls(self):
        return [
            (column, row)
            for row, tiles in enumerate(self.board)
            for column, tile in enumerate(tiles) 
            if tile == TileType.DESTRUCTIBLE]

    def _generate_powerups(self):
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


        return power_ups



    def print_board(self):
        for row in self.board:
            for column in row:
                print(column.value, end="")
            print()

    def _is_horizontal_rail(self, y):
        center = y + PLAYER_SIZE / 2
        row = center // TILE_SIZE
        return row % 2

    def _is_vertical_rail(self, x):
        center = x + PLAYER_SIZE / 2
        col = center // TILE_SIZE
        return col % 2

    def _is_inside(self, row, col):
        if row < 0 or row >= BOARD_ROWS or col < 0 or col >= BOARD_COLS:
            return False
        return True

    def _is_walkable(self, row, col):
        if self._is_inside(row, col):
            return self.board[row][col] == TileType.EMPTY
        return False

    def can_occupy(self, x, y, width, height):
        occupied_cols = []
        occupied_rows = []
        occupied_cols.append(int(x//TILE_SIZE))
        occupied_cols.append(int(((x + width) - 0.000001) // TILE_SIZE))
        occupied_rows.append(int(y//TILE_SIZE))
        occupied_rows.append(int(((y + height) - 0.000001) // TILE_SIZE))
        for row in occupied_rows:
            for col in occupied_cols:
                if  not self._is_walkable(row, col):
                    return False
        return True

    def destroy_tiles(self, affected_tiles):
        for tile in affected_tiles:
            if self.board[tile[1]][tile[0]] == TileType.DESTRUCTIBLE:
                self.board[tile[1]][tile[0]] = TileType.EMPTY

    def _has_fire(self, tile, explosions: list["Explosion"]):
        return any(tile in explosion.active_tiles for explosion in explosions)           

    def draw_powerups(self, screen, explosions: list["Explosion"]):
        for tile, power_up in self.power_ups.items():
            if self.board[tile[1]][tile[0]] == TileType.EMPTY and not self._has_fire(tile, explosions):
                pygame.draw.rect(
                    screen, 
                    "purple",
                    (
                        tile[0] * TILE_SIZE,
                        tile[1] * TILE_SIZE, 
                        TILE_SIZE, 
                        TILE_SIZE)
                    )

    def collect_powerup(self, tile, explosions):
        if tile in self.power_ups:
            if self.board[tile[1]][tile[0]] == TileType.EMPTY and not self._has_fire(tile, explosions):
                return self.power_ups.pop(tile)
        return None

    def destroy_powerups(self, tiles) -> None:
        """Destroy exposed power-ups in newly affected explosion tiles."""
        for tile in tiles:
            if tile in self.power_ups:
                if self.board[tile[1]][tile[0]] == TileType.EMPTY:
                    del self.power_ups[tile]




