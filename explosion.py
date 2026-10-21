import pygame
from player import Player
from constants import TILE_SIZE, EXPLOSION_SIZE, PLAYER_SIZE

class Explosion():

    def __init__(self, affected_tiles):
        self.affected_tiles = affected_tiles
        self.timer = 0.5

    def _initial_position(self, tile):
        x = tile[0] * TILE_SIZE
        y = tile[1] * TILE_SIZE
        return (x, y)

    def hits_player(self, player: Player):

        player_rect = pygame.Rect(
            player.x,
            player.y,
            PLAYER_SIZE,
            PLAYER_SIZE
        )

        for tile in self.affected_tiles:
            x, y = self._initial_position(tile)
            tile_rect = pygame.Rect(
                x,
                y,
                EXPLOSION_SIZE,
                EXPLOSION_SIZE
            )

            if player_rect.colliderect(tile_rect):
                return True
        return False

    def update(self, dt):
        self.timer -= dt

    def draw(self, screen):
        for tile in self.affected_tiles:
            x, y = self._initial_position(tile)
            pygame.draw.rect(screen,"orange", (x, y, EXPLOSION_SIZE, EXPLOSION_SIZE))