import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED, DIRECTIONS

def main():
    # Initialize Pygame (loads internal modules and prepares everything)
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create a Clock object to track time and control FPS
    clock = pygame.time.Clock()

    # Initial coordinates of the player
    player_x = 100.0
    player_y = 100.0
    # This list contain de directions pressed in order. It helps to get a fluent movement.
    pressed_directions =[]

    # Variable to control the main game loop
    running = True

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
            if event.type == pygame.KEYUP:
                if (event.key in DIRECTIONS) and (event.key in pressed_directions):
                    pressed_directions.remove(event.key)


        #2. UPDATE
        keys = pygame.key.get_pressed()
        if pressed_directions:
            direction = pressed_directions[-1]
            vector_direction = DIRECTIONS[direction]
            player_x += vector_direction[0] * PLAYER_SPEED * dt
            player_y += vector_direction[1] * PLAYER_SPEED * dt

        #3. RENDERING
        screen.fill((30, 30, 30)) # Fill the entire screen with dark grey.

        pygame.draw.rect(screen,"blue", (player_x, player_y, 40, 40))

        # Update the display to show everything we just drew
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
