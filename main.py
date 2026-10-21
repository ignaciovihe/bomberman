import pygame
from player import Player
from board import Board
from bomb import Bomb
from explosion import Explosion
from game_state import GameState
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, DIRECTIONS
from ui import screen_game_over

def main():
    # Initialize Pygame (loads internal modules and prepares everything)
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create a Clock object to track time and control FPS
    clock = pygame.time.Clock()

    #Create a new board
    board = Board()

    # Create a new player
    player = Player(1, 45, 45)

    players = {
        1: player
    }

    #This list contain the bombs set by the users
    bombs: list[Bomb] = []

    #This list contain the active explosions.
    explosions: list[Explosion] = []

    # This list contain the directions pressed in order. It helps to get a fluent movement.
    pressed_directions =[]

    # Variable to control the main game loop
    running = True

    # Variable to control the state of the game
    state = GameState.PLAYING

    # Main game loop (each iteration = 1 frame)
    while running:

        milliseconds = clock.tick(60) # Time (in ms) of the last frame; limits the game to 60 FPS
        dt = milliseconds/1000 # Delta time in seconds since the last frame
        
        # 1. Handle events (keyboard, mouse, window close, etc.)
        # Check all events that have happened since the last frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if (event.key in DIRECTIONS) and (event.key not in pressed_directions):
                    pressed_directions.append(event.key)

                if event.key == pygame.K_SPACE:
                    if player.current_bombs < player.max_bombs:
                        new_bomb = Bomb(player.x, player.y, player.id)
                        occupied = any(bomb.tile == new_bomb.tile for bomb in bombs)
                        if not occupied:
                            player.current_bombs += 1
                            bombs.append(new_bomb)

            if event.type == pygame.KEYUP:
                if (event.key in DIRECTIONS) and (event.key in pressed_directions):
                    pressed_directions.remove(event.key)


        #2. UPDATE
        if state == GameState.PLAYING:
            player.update(dt, pressed_directions, board, bombs)

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
                if explosion.hits_player(player):
                    player.alive = False
                explosion.update(dt)

                if explosion.timer <= 0:
                    explosions.remove(explosion)
            if not player.alive:
                state= GameState.GAME_OVER

        #3. RENDERING
        screen.fill((30, 30, 30)) # Fill the entire screen with dark grey.

        board.draw(screen)
        for bomb in bombs:
            bomb.draw(screen)
        for explosion in explosions:
            explosion.draw(screen)
        player.draw(screen)

        if state == GameState.GAME_OVER:
            screen_game_over(screen)

        # Update the display to show everything we just drew
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
