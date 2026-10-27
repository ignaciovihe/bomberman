import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH


def create_menu()-> list[tuple[pygame.Surface, pygame.Rect]]:

    spacing_1 = 25
    spacing_2 = 15

    title_font = pygame.font.Font(None, 50)
    instructions_font = pygame.font.Font(None, 32)
    mode_font = pygame.font.Font(None, 20)

    title = title_font.render("BOMBERMAN", True, "yellow")
    instructions = instructions_font.render("Press ENTER to play", True, "white")
    mode = mode_font.render("2 Players  -  Local Multiplayer", True, "grey")

    total_height = (
        title.get_height()
        + spacing_1
        + instructions.get_height()
        + spacing_2
        + mode.get_height()
    )

    start_y = (SCREEN_HEIGHT - total_height) // 2
    center_x = SCREEN_WIDTH // 2

    title_rect = title.get_rect(midtop=(center_x, start_y))
    instructions_rect = instructions.get_rect(midtop=(center_x, title_rect.bottom + spacing_1))
    mode_rect = mode.get_rect(midtop=(center_x, instructions_rect.bottom + spacing_2))

    return [
        (title, title_rect),
        (instructions , instructions_rect),
        (mode, mode_rect)
    ]

def screen_menu(screen: pygame.Surface, menu_items: list[tuple[pygame.Surface, pygame.Rect]]) -> None:
    for text, rect in menu_items:
        screen.blit(text,rect)


def screen_game_over(screen: pygame.Surface, winner):
    font = pygame.font.Font(None, 64)
    if winner == 0:
        text = font.render("DRAW", True, "white")
    elif winner == 1:
        text = font.render("PLAYER 1 WINS", True, "white")
    else:
        text = font.render("PLAYER 2 WINS", True, "white")
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text,text_rect)