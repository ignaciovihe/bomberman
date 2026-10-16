from constants import DIRECTIONS, PLAYER_SPEED, PLAYER_SIZE, TILE_SIZE
from board import Board
import pygame

# Represents a player in the game
class Player():

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def draw(self, screen):
        pygame.draw.rect(screen,"blue", (self.x, self.y, PLAYER_SIZE, PLAYER_SIZE))

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
        return (aligned_rail - 5 <= current_pos <= aligned_rail +5)

    def update(self, dt, pressed_directions, board: Board):
        if pressed_directions:
            desire_direction = pressed_directions[-1]
            vector_direction = DIRECTIONS[desire_direction]
            if (desire_direction == pygame.K_RIGHT or desire_direction == pygame.K_LEFT):
                aligned_y = self._aligned_y()
                if self._is_inside_margin(aligned_y, self.y) and board._is_walkable_row(self.y):
                    desired_x = self.x + vector_direction[0] * PLAYER_SPEED * dt
                    desired_y = aligned_y
                    if board.can_occupy(desired_x, desired_y, PLAYER_SIZE, PLAYER_SIZE):
                        self.x = desired_x
                        self.y = desired_y
            if (desire_direction == pygame.K_UP or desire_direction == pygame.K_DOWN):
                aligned_x = self._aligned_x()
                if self._is_inside_margin(aligned_x, self.x) and board._is_walkable_col(self.x):
                    desired_x = aligned_x
                    desired_y = self.y + vector_direction[1] * PLAYER_SPEED * dt
                    if board.can_occupy(desired_x, desired_y, PLAYER_SIZE, PLAYER_SIZE):
                        self.x = desired_x
                        self.y = desired_y

