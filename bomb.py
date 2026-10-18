from constants import PLAYER_SIZE, BOMB_RADIUS,TILE_SIZE
import pygame

class Bomb():

    def __init__(self, x, y, id_player):
        self.x = x
        self.y = y
        self.tile = self._calculate_tile()
        self.center = self._calculate_tile_center()
        self.id_player = id_player

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

    def draw(self, screen):
        pygame.draw.circle(screen, "black", self.center, BOMB_RADIUS)
        