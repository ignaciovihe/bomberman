import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH


def create_menu()-> list[tuple[pygame.Surface, pygame.Rect]]:

    spacing_1 = 25
    spacing_2 = 15

    title_font = pygame.font.SysFont("dejavusans", 50)
    instructions_font = pygame.font.SysFont("dejavusans", 32)
    mode_font = pygame.font.SysFont("dejavusans", 20)

    title = title_font.render("BOMBERMAN", True, "#F4C95D")
    instructions = instructions_font.render("Press ENTER to play", True, "#FFFFFF")
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


def create_game_over(screen: pygame.Surface, winner):

    spacing = 25
    
    winner_font = pygame.font.SysFont("dejavusans", 32, bold=True)
    instructions_font = pygame.font.SysFont("dejavusans", 20)

    if winner == 0:
        winner_text = winner_font.render("DRAW", True, "#F4C95D")
    elif winner == 1:
        winner_text = winner_font.render("PLAYER BLUE WINS", True, "#F4C95D")
    else:
        winner_text = winner_font.render("PLAYER RED WINS", True, "#F4C95D") 
    instructions = instructions_font.render("Press R to play again", True, "#FFFFFF")

    total_height = (
        winner_text.get_height()
        + spacing
        + instructions.get_height()
    )

    start_y = (SCREEN_HEIGHT - total_height) // 2
    center_x = SCREEN_WIDTH // 2

    winner_rect = winner_text.get_rect(midtop=(center_x, start_y))
    instructions_rect = instructions.get_rect(midtop=(center_x, winner_rect.bottom + spacing))
    background_rect = winner_rect.union(instructions_rect)
    background_rect = background_rect.inflate(40, 40)

    return [
        (winner_text, winner_rect),
        (instructions , instructions_rect)
    ], background_rect

def screen_game_over(screen: pygame.Surface, game_over_items: list[tuple[pygame.Surface, pygame.Rect]], background) -> None:
    pygame.draw.rect(screen, "#202632", background, border_radius=12)
    for text, rect in game_over_items:
        screen.blit(text,rect)