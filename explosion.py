import pygame
from player import Player
from constants import TILE_SIZE, EXPLOSION_SIZE, EXPLOSION_HOLD_TIME, EXPANSION_INTERVAL, PLAYER_SIZE

class Explosion():

    def __init__(self, origin_tile, affected_tiles):
        self.origin_tile = origin_tile
        self.affected_tiles = affected_tiles
        self.active_tiles = [self.origin_tile]
        self.explosion_duration = self._calculate_max_distance() * EXPANSION_INTERVAL + EXPLOSION_HOLD_TIME
        self.timer = self.explosion_duration

    def _initial_position(self, tile):
        x = tile[0] * TILE_SIZE
        y = tile[1] * TILE_SIZE
        return (x, y)

    def _calculate_distance(self, tile):
        return abs(tile[0] - self.origin_tile[0]) + abs((tile[1] - self.origin_tile[1]))

    def _calculate_max_distance(self):
        max_distance = 0
        for tile in self.affected_tiles:
            current_distance = self._calculate_distance(tile)
            if current_distance > max_distance:
                max_distance = current_distance
        return max_distance

    def _update_active_tiles(self, max_distance):
        for tile in self.affected_tiles:
            if self._calculate_distance(tile) <= max_distance and tile not in self.active_tiles:
                self.active_tiles.append(tile)    
            


    def hits_player(self, player: Player):

        player_rect = pygame.Rect(
            player.x,
            player.y,
            PLAYER_SIZE,
            PLAYER_SIZE
        )

        for tile in self.active_tiles:
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
        elapsed_time = self.explosion_duration - self.timer
        max_distance = int((elapsed_time + 1e-9) / EXPANSION_INTERVAL)
        self._update_active_tiles(max_distance)

    def draw(self, screen):
        for tile in self.active_tiles:
            x, y = self._initial_position(tile)
            pygame.draw.rect(screen,"orange", (x, y, EXPLOSION_SIZE, EXPLOSION_SIZE))