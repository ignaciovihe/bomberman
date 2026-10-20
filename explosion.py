import pygame
from constants import TILE_SIZE, EXPLOSION_SIZE

class Explosion():

    def __init__(self, affected_tiles):
        self.affected_tiles = affected_tiles
        self.timer = 0.5

    def _initial_position(self, tile):
        x = tile[0] * TILE_SIZE
        y = tile[1] * TILE_SIZE
        return (x, y)

    def update(self, dt):
        self.timer -= dt

    def draw(self, screen):
        for tile in self.affected_tiles:
            x, y = self._initial_position(tile)
            pygame.draw.rect(screen,"orange", (x, y, EXPLOSION_SIZE, EXPLOSION_SIZE))