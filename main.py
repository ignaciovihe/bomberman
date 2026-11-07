
import pygame
from player import Player
from board import Board
from bomb import Bomb
from explosion import Explosion
from game_state import GameState
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, DIRECTIONS_P1, DIRECTIONS_P2
from ui import screen_game_over, screen_menu, create_menu, create_game_over
from assets import (
    load_powerup_images,
    load_bomb_image,
    load_explosion_images,
    load_tiles_images,
    load_playe1_images,
    load_playe2_images
)


def place_bomb(player: Player, bombs: list[Bomb]) -> None:
    """Place a bomb if the player has capacity and the tile is unoccupied."""
    if player.current_bombs < player.max_bombs:
        new_bomb = Bomb(player.x, player.y, player.id, player.fire_power)
        occupied = any(bomb.tile == new_bomb.tile for bomb in bombs)
        if not occupied:
            player.current_bombs += 1
            bombs.append(new_bomb)


def trigger_chain_reactions(
    affected_tiles: list[tuple[int, int]],
    bombs: list[Bomb]
) -> None:
    """Trigger bombs located on tiles reached by an explosion."""
    for bomb in bombs:
        if bomb.tile in affected_tiles:
            bomb.timer = 0


def new_game() -> tuple[
    Board,
    dict[int, Player],
    list[Bomb],
    list[Explosion],
    dict[int, list[str]]
]:
    """Create a new game with a fresh board, players, and empty game objects."""

    # Create a new board.
    board = Board()

    # Create the two players at their starting positions.
    player = Player(1, 45, 45)
    player_2 = Player(2, 525, 445)

    players = {
        1: player,
        2: player_2
    }

    # Store bombs currently placed by the players.
    bombs: list[Bomb] = []

    # Store active explosions.
    explosions: list[Explosion] = []

    # Track pressed directions in order to prioritize the latest input.
    pressed_directions = {
        1: [],
        2: []
    }

    return board, players, bombs, explosions, pressed_directions


def main() -> None:
    """Initialize the game and run its event, update, and rendering loop."""

    # Initialize Pygame and create the game window.
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Load graphical assets.
    powerup_surfaces = load_powerup_images()
    bomb_surface = load_bomb_image()
    explosion_surfaces = load_explosion_images()
    tile_surfaces = load_tiles_images()
    player1_surfaces = load_playe1_images()
    player2_surfaces = load_playe2_images()

    # Prepare the menu text surfaces and their positions.
    items_menu = create_menu()

    # Create a clock to track elapsed time and limit the frame rate.
    clock = pygame.time.Clock()

    # Initialize the board, players, and game objects.
    board, players, bombs, explosions, pressed_directions = new_game()

    # Control the main game loop.
    running = True

    # Track the current game state.
    state = GameState.MENU

    # Store the winner: 0 for a draw, 1 or 2 for the winning player.
    winner = None

    # Delay the game-over screen to display player death animations.
    resolving_timer = 0.3

    # Main game loop (one iteration per frame).
    while running:

        # Limit the game to 60 FPS and calculate delta time in seconds.
        milliseconds = clock.tick(60)
        dt = milliseconds / 1000

        # 1. HANDLE EVENTS
        # Process window events and keyboard input.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Start the game when ENTER is pressed in the main menu.
            if state == GameState.MENU:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        state = GameState.PLAYING

            # Handle movement and bomb placement during active game states.
            elif state in (GameState.PLAYING, GameState.RESOLVING):
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

            # Remove released directions from the pressed-key lists.
            if event.type == pygame.KEYUP:
                if (event.key in DIRECTIONS_P1) and (DIRECTIONS_P1[event.key] in pressed_directions[1]):
                    pressed_directions[1].remove(DIRECTIONS_P1[event.key])

                if (event.key in DIRECTIONS_P2) and (DIRECTIONS_P2[event.key] in pressed_directions[2]):
                    pressed_directions[2].remove(DIRECTIONS_P2[event.key])

            # Restart the game when R is pressed after a match.
            if state == GameState.GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        board, players, bombs, explosions, pressed_directions = new_game()
                        winner = None
                        state = GameState.PLAYING
                        resolving_timer = 0.3

        # 2. UPDATE
        # Update players, bombs, and explosions during active game states.
        if state in (GameState.PLAYING, GameState.RESOLVING):

            # Update living players and collect available power-ups.
            for id_player, current_player in players.items():
                if current_player.alive:
                    current_player.update(dt, pressed_directions[id_player], board, bombs)
                    player_tile = current_player.get_tile()
                    power_up = board.collect_powerup(player_tile, explosions)
                    if power_up:
                        current_player.apply_powerup(power_up)

            # Update bomb timers and create explosions when bombs detonate.
            for bomb in bombs[:]:
                bomb.update(dt)

                if bomb.timer <= 0:
                    affected_tiles = bomb.check_explosions(board)
                    bombs.remove(bomb)
                    players[bomb.id_player].current_bombs -= 1
                    explosion = Explosion(bomb.tile, affected_tiles)
                    explosions.append(explosion)
                    continue

                # Prevent the bomb owner from passing through after leaving it.
                owner = players[bomb.id_player]

                if bomb.owner_can_pass and not bomb.overlaps_player(owner.x, owner.y):
                    bomb.owner_can_pass = False

            # Update explosions, destroy objects, and check player damage.
            for explosion in explosions[:]:
                current_active_tiles = explosion.update(dt)
                board.destroy_powerups(current_active_tiles)
                board.destroy_tiles(current_active_tiles)
                trigger_chain_reactions(current_active_tiles, bombs)

                for current_player in players.values():
                    if explosion.hits_player(current_player):
                        current_player.alive = False

                # Remove expired explosions.
                if explosion.timer <= 0:
                    explosions.remove(explosion)

        # Enter the resolving state when at least one player dies.
        if state == GameState.PLAYING:
            if not players[1].alive or not players[2].alive:
                state = GameState.RESOLVING

        # Determine the winner after the resolving delay.
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
                items_game_over, background_rect = create_game_over(screen, winner)

        # 3. RENDERING
        # Clear the screen before drawing the current frame.
        screen.fill((30, 30, 30))

        if state == GameState.MENU:
            screen_menu(screen, items_menu)
        else:
            # Draw the board, power-ups, bombs, and explosions.
            board.draw(screen, tile_surfaces)
            board.draw_powerups(screen, explosions, powerup_surfaces)

            for bomb in bombs:
                bomb.draw(screen, bomb_surface)

            for explosion in explosions:
                explosion.draw(screen, explosion_surfaces)

            # Draw both players using their respective sprite collections.
            for id_player, current_player in players.items():
                if id_player == 1:
                    current_player.draw(screen, player1_surfaces)
                else:
                    current_player.draw(screen, player2_surfaces)

            # Display the game-over overlay when the match ends.
            if state == GameState.GAME_OVER:
                screen_game_over(screen, items_game_over, background_rect)

        # Present the completed frame.
        pygame.display.flip()

    # Release Pygame resources when the main loop ends.
    pygame.quit()


if __name__ == "__main__":
    main()
