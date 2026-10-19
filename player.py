from constants import DIRECTIONS, PLAYER_SPEED, PLAYER_SIZE, TILE_SIZE, PLAYER_MOVE_MARGIN
from board import Board
from bomb import Bomb
import pygame

# Represents a player in the game
class Player():

    def __init__(self,id, x, y):
        self.id = id
        self.x = float(x)
        self.y = float(y)
        self.current_direction = None
        self.current_bombs = 0
        self.max_bombs = 1

    def _aligned_y(self):
        center = self.y + PLAYER_SIZE / 2
        row = center // TILE_SIZE
        top_edge = row * TILE_SIZE
        margin = (TILE_SIZE - PLAYER_SIZE) / 2
        return top_edge + margin

    def _aligned_x(self):
        center = self.x + PLAYER_SIZE / 2
        col = center // TILE_SIZE
        left_edge = col * TILE_SIZE
        margin = (TILE_SIZE - PLAYER_SIZE) / 2
        return left_edge + margin

    def _is_inside_margin(self, aligned_rail, current_pos):
        return (aligned_rail - PLAYER_MOVE_MARGIN <= current_pos <= aligned_rail + PLAYER_MOVE_MARGIN)

    def _can_move_through_bombs(self, x, y, bombs: list[Bomb]):
        for bomb in bombs:
            if bomb.overlaps_player(x, y):
                if bomb.id_player != self.id or not bomb.owner_can_pass:
                    return False
        return True

    def _move(self, dt, direction, vector_d, board: Board, bombs: list[Bomb]):
        if (direction == pygame.K_RIGHT or direction == pygame.K_LEFT):
            aligned_y = self._aligned_y()
            if self._is_inside_margin(aligned_y, self.y) and board._is_horizontal_rail(self.y):
                desired_x = self.x + vector_d[0] * PLAYER_SPEED * dt
                desired_y = aligned_y
                if board.can_occupy(desired_x, desired_y, PLAYER_SIZE, PLAYER_SIZE):
                    if self._can_move_through_bombs(desired_x, desired_y, bombs):
                        self.x = desired_x
                        self.y = desired_y
                        return True
        if (direction == pygame.K_UP or direction == pygame.K_DOWN):
            aligned_x = self._aligned_x()
            if self._is_inside_margin(aligned_x, self.x) and board._is_vertical_rail(self.x):
                desired_x = aligned_x
                desired_y = self.y + vector_d[1] * PLAYER_SPEED * dt
                if board.can_occupy(desired_x, desired_y, PLAYER_SIZE, PLAYER_SIZE):
                    if self._can_move_through_bombs(desired_x, desired_y, bombs):
                        self.x = desired_x
                        self.y = desired_y
                        return True
        return False


    def update(self, dt, pressed_directions, board: Board, bombs: list[Bomb]):
        if pressed_directions:
            desire_direction = pressed_directions[-1]
            vector_direction = DIRECTIONS[desire_direction]
            
            can_move = self._move(dt, desire_direction, vector_direction, board, bombs)

            if can_move:
                self.current_direction = desire_direction
            else:
                if self.current_direction in pressed_directions:
                    vector_direction = DIRECTIONS[self.current_direction]

                    can_move = self._move(dt, self.current_direction, vector_direction, board, bombs)
        else:
            self.current_direction = None

    def draw(self, screen):
        pygame.draw.rect(screen,"blue", (self.x, self.y, PLAYER_SIZE, PLAYER_SIZE))

