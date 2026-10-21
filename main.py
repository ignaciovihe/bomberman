import pygame
from player import Player
from board import Board
from bomb import Bomb
from explosion import Explosion
from game_state import GameState
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, DIRECTIONS_P1, DIRECTIONS_P2, PLAYER_COLOR
from ui import screen_game_over

def place_bomb(player: Player, bombs: list[Bomb]):
    if player.current_bombs < player.max_bombs:
        new_bomb = Bomb(player.x, player.y, player.id)
        occupied = any(bomb.tile == new_bomb.tile for bomb in bombs)
        if not occupied:
            player.current_bombs += 1
            bombs.append(new_bomb)


def main():
    # Initialize Pygame (loads internal modules and prepares everything)
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create a Clock object to track time and control FPS
    clock = pygame.time.Clock()

    #Create a new board
    board = Board()

    # Create the new players
    player = Player(1, 45, 45)
    player_2 = Player(2, 525, 445)

    players = {
        1: player,
        2: player_2
    }

    # This list contain the directions pressed in order. It helps to get a fluent movement.
    pressed_directions ={
        1: [],
        2: []
    }

    #This list contain the bombs set by the users
    bombs: list[Bomb] = []

    #This list contain the active explosions.
    explosions: list[Explosion] = []

    # Variable to control the main game loop
    running = True

    # Variable to control the state of the game
    state = GameState.PLAYING

    # Variable to set the winner
    winner = None

    # Variable that contains the time of the resolving state.
    resolving_timer = 0.3

    # Main game loop (each iteration = 1 frame)
    while running:

        milliseconds = clock.tick(60) # Time (in ms) of the last frame; limits the game to 60 FPS
        dt = milliseconds/1000 # Delta time in seconds since the last frame
        
        # 1. Handle events (keyboard, mouse, window close, etc.)
        # Check all events that have happened since the last frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if state == GameState.PLAYING:
                if event.type == pygame.KEYDOWN:
                    if (event.key in DIRECTIONS_P1) and (DIRECTIONS_P1[event.key] not in pressed_directions[1]):
                        pressed_directions[1].append(DIRECTIONS_P1[event.key])

                    if (event.key in DIRECTIONS_P2) and (DIRECTIONS_P2[event.key] not in pressed_directions[2]):
                        pressed_directions[2].append(DIRECTIONS_P2[event.key])

                    if event.key == pygame.K_SPACE:
                        place_bomb(players[1], bombs)

                    if event.key == pygame.K_q:
                        place_bomb(players[2], bombs)

            if event.type == pygame.KEYUP:
                if (event.key in DIRECTIONS_P1) and (DIRECTIONS_P1[event.key] in pressed_directions[1]):
                    pressed_directions[1].remove(DIRECTIONS_P1[event.key])

                if (event.key in DIRECTIONS_P2) and (DIRECTIONS_P2[event.key] in pressed_directions[2]):
                    pressed_directions[2].remove(DIRECTIONS_P2[event.key])


        #2. UPDATE
        if state == GameState.PLAYING:
            for id_player, current_player in players.items():
                current_player.update(dt, pressed_directions[id_player], board, bombs)

        if state == GameState.PLAYING or state == GameState.RESOLVING:
            for bomb in bombs[:]:
                bomb.update(dt)

                if bomb.timer <= 0:
                    affected_tiles = bomb.check_explosions(board)
                    bombs.remove(bomb)
                    players[bomb.id_player].current_bombs -=1
                    explosion = Explosion(affected_tiles)
                    explosions.append(explosion)
                    board.destroy_tiles(affected_tiles)
                    continue

                owner = players[bomb.id_player]

                if bomb.owner_can_pass and not bomb.overlaps_player(owner.x, owner.y):
                    bomb.owner_can_pass = False

            for explosion in explosions[:]:
                for current_player in players.values():
                    if explosion.hits_player(current_player):
                        current_player.alive = False
                explosion.update(dt)

                if explosion.timer <= 0:
                    explosions.remove(explosion)

        if state == GameState.PLAYING:    
            if not players[1].alive or not players[2].alive:
                state = GameState.RESOLVING

        elif state == GameState.RESOLVING:
            resolving_timer -= dt
            if resolving_timer <= 0:
                if not players[1].alive and not players[2].alive:
                    winner = 0
                elif not players[1].alive:
                    winner = 2
                elif not players[2].alive:
                    winner = 1
                state = GameState.GAME_OVER

        #3. RENDERING
        screen.fill((30, 30, 30)) # Fill the entire screen with dark grey.

        board.draw(screen)
        for bomb in bombs:
            bomb.draw(screen)
        for explosion in explosions:
            explosion.draw(screen)
        for id_player, current_player in players.items():
            current_player.draw(screen, PLAYER_COLOR[id_player])

        if state == GameState.GAME_OVER:
            screen_game_over(screen, winner)

        # Update the display to show everything we just drew
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
