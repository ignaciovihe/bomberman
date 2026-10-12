from constants import DIRECTIONS, PLAYER_SPEED
import pygame

# Represents a player in the game
class Player():

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def draw(self, screen):
        pygame.draw.rect(screen,"blue", (self.x, self.y, 40, 40))

    def update(self, dt, pressed_directions):
        if pressed_directions:
            direction = pressed_directions[-1]
            vector_direction = DIRECTIONS[direction]
            self.x += vector_direction[0] * PLAYER_SPEED * dt
            self.y += vector_direction[1] * PLAYER_SPEED * dt
