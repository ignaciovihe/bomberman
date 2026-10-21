import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

def screen_game_over(screen, winner):
    font = pygame.font.Font(None, 64)
    if winner == 0:
        text = font.render("DRAW", True, "white")
    elif winner == 1:
        text = font.render("PLAYER 1 WINS", True, "white")
    else:
        text = font.render("PLAYER 2 WINS", True, "white")
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text,text_rect)