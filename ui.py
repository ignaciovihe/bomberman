import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

def screen_game_over(screen):
    font = pygame.font.Font(None, 64)
    text = font.render("GAME OVER", True, "white")
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text,text_rect)