
import pygame
from player import Player
from constants import TILE_SIZE, EXPLOSION_SIZE, EXPLOSION_HOLD_TIME, EXPANSION_INTERVAL, PLAYER_SIZE


class Explosion():
    """Represent an explosion that progressively expands across affected tiles."""

    def __init__(self, origin_tile: tuple[int, int], affected_tiles: list[tuple[int, int]]) -> None:
        """Initialize an explosion with its origin, affected tiles, and duration.

        Args:
            origin_tile: Tile (col, row) where the explosion starts.
            affected_tiles: Tiles reached by the explosion.
        """
        self.origin_tile = origin_tile
        self.affected_tiles = affected_tiles
        self.active_tiles = [self.origin_tile]
        self.explosion_duration = self._calculate_max_distance() * EXPANSION_INTERVAL + EXPLOSION_HOLD_TIME
        self.timer = self.explosion_duration

    def _initial_position(self, tile: tuple[int, int]) -> tuple[int, int]:
        """Return the top-left pixel position of a tile.

        Args:
            tile: Tile coordinates as (col, row).
        """
        x = tile[0] * TILE_SIZE
        y = tile[1] * TILE_SIZE
        return (x, y)

    def _calculate_distance(self, tile: tuple[int, int]) -> int:
        """Calculate the Manhattan distance from the explosion origin to a tile.

        Args:
            tile: Tile coordinates as (col, row).

        Returns:
            int: Distance measured in tiles.
        """
        return abs(tile[0] - self.origin_tile[0]) + abs((tile[1] - self.origin_tile[1]))

    def _calculate_max_distance(self) -> int:
        """Return the maximum distance reached by the explosion in tiles."""
        max_distance = 0
        for tile in self.affected_tiles:
            current_distance = self._calculate_distance(tile)
            if current_distance > max_distance:
                max_distance = current_distance
        return max_distance

    def _update_active_tiles(self, max_distance: int) -> list[tuple[int, int]]:
        """Activate tiles reached by the explosion's current expansion distance.

        Args:
            max_distance: Maximum distance currently reached by the explosion.

        Returns:
            list[tuple[int, int]]: Newly activated tiles.
        """
        new_active_tiles = []
        for tile in self.affected_tiles:
            if self._calculate_distance(tile) <= max_distance and tile not in self.active_tiles:
                self.active_tiles.append(tile)
                new_active_tiles.append(tile)
        return new_active_tiles

    def hits_player(self, player: Player) -> bool:
        """Check whether any active explosion tile overlaps a player.

        Args:
            player: Player to check for collision.

        Returns:
            bool: True if the explosion hits the player.
        """
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

    def update(self, dt: float) -> list[tuple[int, int]]:
        """Update the explosion timer and progressively activate affected tiles.

        Args:
            dt: Time elapsed since the previous frame in seconds.

        Returns:
            list[tuple[int, int]]: Tiles activated during this update.
        """
        self.timer -= dt
        elapsed_time = self.explosion_duration - self.timer
        max_distance = int((elapsed_time + 1e-9) / EXPANSION_INTERVAL)
        new_active_tiles = self._update_active_tiles(max_distance)
        return new_active_tiles

    def draw(self, screen: pygame.Surface, surfaces: dict[str, pygame.Surface]) -> None:
        """Draw explosion sprites on all currently active tiles.

        Args:
            screen: Pygame surface on which to draw the explosion.
            surfaces: Dictionary containing center, horizontal, and vertical sprites.
        """
        for tile in self.active_tiles:
            x, y = self._initial_position(tile)
            #pygame.draw.rect(screen,"orange", (x, y, EXPLOSION_SIZE, EXPLOSION_SIZE))
            if tile == self.origin_tile:
                screen.blit(surfaces["center"], (x, y))
            if tile[0] != self.origin_tile[0]:
                screen.blit(surfaces["horizontal"], (x, y))
            else:
                screen.blit(surfaces["vertical"], (x, y))
