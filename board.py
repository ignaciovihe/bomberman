from tile import TileType
from constants import BOARD_COLS, BOARD_ROWS, TILE_COLORS, TILE_SIZE
import pygame

class Board():

    def __init__(self):
        self.board = self._generate_board()

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
                else:
                    row.append(TileType.EMPTY)
            board.append(row)
        return board

    def print_board(self):
        for row in self.board:
            for column in row:
                print(column.value, end="")
            print()

    def _is_inside(self, row, col):
        if row < 0 or row >= BOARD_ROWS or col < 0 or col >= BOARD_COLS:
            return False
        return True

    def is_walkable(self, row, col):
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
                if  not self.is_walkable(row, col):
                    return False
        return True

