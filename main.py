import pygame
from player import Player
from board import Board
from bomb import Bomb
from explosion import Explosion
from game_state import GameState
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, DIRECTIONS_P1, DIRECTIONS_P2, PLAYER_COLOR
from ui import screen_game_over
from pprint import pprint
from tile import TileType
from assets import load_powerup_images, load_bomb_image, load_explosion_images, load_tiles_images, load_playe1_images, load_playe2_images

def place_bomb(player: Player, bombs: list[Bomb]):
    if player.current_bombs < player.max_bombs:
        new_bomb = Bomb(player.x, player.y, player.id, player.fire_power)
        occupied = any(bomb.tile == new_bomb.tile for bomb in bombs)
        if not occupied:
            player.current_bombs += 1
            bombs.append(new_bomb)

def trigger_chain_reactions(affected_tiles, bombs: list[Bomb]):
    for bomb in bombs:
        if bomb.tile in affected_tiles:
            bomb.timer = 0


def main():
    # Initialize Pygame (loads internal modules and prepares everything)
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Load images
    powerup_surfaces = load_powerup_images()
    bomb_surface = load_bomb_image()
    explosion_surfaces = load_explosion_images()
    tile_surfaces = load_tiles_images()
    player1_surfaces = load_playe1_images()
    player2_surfaces = load_playe2_images()

    # Create a Clock object to track time and control FPS
    clock = pygame.time.Clock()

    #Create a new board
    board = Board()
    pprint(board.power_ups)

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
            if state in (GameState.PLAYING, GameState.RESOLVING):
                if event.type == pygame.KEYDOWN:
                    if (event.key in DIRECTIONS_P1) and (DIRECTIONS_P1[event.key] not in pressed_directions[1]):
                        pressed_directions[1].append(DIRECTIONS_P1[event.key])

                    if (event.key in DIRECTIONS_P2) and (DIRECTIONS_P2[event.key] not in pressed_directions[2]):
                        pressed_directions[2].append(DIRECTIONS_P2[event.key])

                    if state == GameState.PLAYING:
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
        if state in (GameState.PLAYING, GameState.RESOLVING):
            for id_player, current_player in players.items():
                if current_player.alive:
                    current_player.update(dt, pressed_directions[id_player], board, bombs)
                    player_tile = current_player.get_tile()
                    power_up = board.collect_powerup(player_tile, explosions)
                    if power_up:
                        current_player.apply_powerup(power_up)
                    
            for bomb in bombs[:]:
                bomb.update(dt)

                if bomb.timer <= 0:
                    affected_tiles = bomb.check_explosions(board)
                    bombs.remove(bomb)
                    players[bomb.id_player].current_bombs -=1
                    explosion = Explosion(bomb.tile ,affected_tiles)
                    explosions.append(explosion)
                    continue

                owner = players[bomb.id_player]

                if bomb.owner_can_pass and not bomb.overlaps_player(owner.x, owner.y):
                    bomb.owner_can_pass = False

            for explosion in explosions[:]:
                current_active_tiles = explosion.update(dt)
                board.destroy_powerups(current_active_tiles)
                board.destroy_tiles(current_active_tiles)
                trigger_chain_reactions(current_active_tiles, bombs)
                for current_player in players.values():
                    if explosion.hits_player(current_player):
                        current_player.alive = False


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

        board.draw(screen, tile_surfaces)
        board.draw_powerups(screen, explosions, powerup_surfaces)
        for bomb in bombs:
            bomb.draw(screen, bomb_surface)
        for explosion in explosions:
            explosion.draw(screen, explosion_surfaces)
        for id_player, current_player in players.items():
            if id_player == 1:
                current_player.draw(screen, player1_surfaces)
            else:
                current_player.draw(screen, player2_surfaces)

        if state == GameState.GAME_OVER:
            screen_game_over(screen, winner)

        # Update the display to show everything we just drew
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
