from constants import POWERUP_IMAGES, TILE_SIZE
from power_up import PowerUp
import pygame

def load_powerup_images() -> dict[PowerUp, pygame.Surface]:
    loaded_images = {}
    for power_up, path in POWERUP_IMAGES.items():
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        loaded_images[power_up] = image
    return loaded_images

