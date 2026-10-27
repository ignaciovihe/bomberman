from constants import PLAYER_SIZE, TILE_SIZE, EXPLOSION_DIRECTIONS
from board import Board
from tile import TileType
import pygame

class Bomb():

    def __init__(self, x, y, id_player, power):
        self.x = x
        self.y = y
        self.tile = self._calculate_tile()
        self.center = self._calculate_tile_center()
        self.id_player = id_player
        self.timer = 3.0
        self.owner_can_pass = True
        self.power = power

    def _calculate_tile(self):
        player_center_x = self.x + PLAYER_SIZE / 2
        player_center_y = self.y + PLAYER_SIZE / 2
        bomb_tile_x = int(player_center_x // TILE_SIZE)
        bomb_tile_y = int(player_center_y // TILE_SIZE)
        return (bomb_tile_x, bomb_tile_y)

    def _calculate_tile_center(self):
        
        bomb_x = (self.tile[0] * TILE_SIZE) + TILE_SIZE / 2
        bomb_y = (self.tile[1] * TILE_SIZE) + TILE_SIZE / 2
        return (bomb_x, bomb_y)

    def overlaps_player(self, x, y):
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

    def check_explosions(self, board: Board):
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

    def update(self, dt):
        self.timer -= dt

    def draw(self, screen, surface):
        screen.blit(surface, (self.tile[0] * TILE_SIZE, self.tile[1] * TILE_SIZE))
        