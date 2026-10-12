from tile import TileType
from constants import BOARD_COLS, BOARD_ROWS, TILE_COLORS, TILE_SIZE
import pygame

class Board():

    def __init__(self):
        self.board = self._generate_board()
        self.print_board()

    def draw(self, screen):
        for row_index, row in enumerate(self.board):
            for column_index, tile in enumerate(row):
                pygame.draw.rect(screen, TILE_COLORS[tile], (column_index * TILE_SIZE, row_index * TILE_SIZE, TILE_SIZE, TILE_SIZE))


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
            


