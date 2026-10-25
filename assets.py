from constants import (
    POWERUP_IMAGES, 
    TILE_SIZE, 
    BOMB_IMAGE, 
    EXPLOSION_IMAGES, 
    TILE_IMAGES, 
    PLAYER1_IMAGES, 
    PLAYER2_IMAGES
    )
from power_up import PowerUp
import pygame

def load_powerup_images() -> dict[PowerUp, pygame.Surface]:
    loaded_images = {}
    for power_up, path in POWERUP_IMAGES.items():
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        loaded_images[power_up] = image
    return loaded_images

def load_bomb_image() -> pygame.Surface:
    image = pygame.image.load(BOMB_IMAGE).convert_alpha()
    image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
    return image

def load_explosion_images() -> dict[PowerUp, pygame.Surface]:
    loaded_images = {}
    for explosion_type, path in EXPLOSION_IMAGES.items():
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        loaded_images[explosion_type] = image
    return loaded_images

def load_tiles_images() -> dict[PowerUp, pygame.Surface]:
    loaded_images = {}
    for tile_type, path in TILE_IMAGES.items():
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        loaded_images[tile_type] = image
    return loaded_images

def load_playe1_images() -> dict[PowerUp, pygame.Surface]:
    loaded_images = {}
    for direction, path in PLAYER1_IMAGES.items():
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        loaded_images[direction] = image
    return loaded_images

def load_playe2_images() -> dict[PowerUp, pygame.Surface]:
    loaded_images = {}
    for direction, path in PLAYER2_IMAGES.items():
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        loaded_images[direction] = image
    return loaded_images
