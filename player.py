
from constants import (
    DIRECTIONS, 
    PLAYER_SIZE, 
    TILE_SIZE, 
    PLAYER_MOVE_MARGIN, 
    SPEED_UP_INCREMENT, 
    INITIAL_PLAYER_SPPED, 
    MAX_PLAYER_SPEED,
    )

from board import Board
from bomb import Bomb
from power_up import PowerUp

# Represents a player in the game
class Player():

    def __init__(self,id, x, y) -> None:
        """Initialize a player with its position and initial attributes."""
        self.id = id
        self.x = float(x)
        self.y = float(y)
        self.current_direction = None
        self.current_bombs = 0
        self.max_bombs = 1
        self.fire_power = 1
        self.speed = INITIAL_PLAYER_SPPED
        self.alive = True

    def _aligned_y(self) -> float:
        """Return the Y position aligned with the nearest horizontal tile corridor."""
        center = self.y + PLAYER_SIZE / 2
        row = center // TILE_SIZE
        top_edge = row * TILE_SIZE
        margin = (TILE_SIZE - PLAYER_SIZE) / 2
        return top_edge + margin

    def _aligned_x(self) -> float:
        """Return the X position aligned with the nearest vertical tile corridor."""
        center = self.x + PLAYER_SIZE / 2
        col = center // TILE_SIZE
        left_edge = col * TILE_SIZE
        margin = (TILE_SIZE - PLAYER_SIZE) / 2
        return left_edge + margin

    def _is_inside_margin(self, aligned_rail, current_pos) -> bool:
        """Check whether a position is within the allowed alignment margin.

        Args:
            aligned_rail: Target aligned position.
            current_pos: Current position on the same axis.

        Returns:
            bool: True if the position is within the margin.
        """
        return (aligned_rail - PLAYER_MOVE_MARGIN <= current_pos <= aligned_rail + PLAYER_MOVE_MARGIN)

    def _can_move_through_bombs(self, x, y, bombs: list[Bomb]) -> bool:
        """Check whether the player can move to a position without being blocked by bombs.

        Args:
            x: Desired X position in pixels.
            y: Desired Y position in pixels.
            bombs: Currently placed bombs.

        Returns:
            bool: True if no bomb blocks the movement.
        """
        for bomb in bombs:
            if bomb.overlaps_player(x, y):
                if bomb.id_player != self.id or not bomb.owner_can_pass:
                    return False
        return True

    def get_center(self) -> tuple[float, float]:
        """Return the player's center position in pixels."""
        x = self.x + PLAYER_SIZE / 2
        y = self.y + PLAYER_SIZE / 2
        return (x,y)

    def get_tile(self) -> tuple[int, int]:
        """Return the tile (col, row) containing the player's center."""
        center = self.get_center()
        x = int(center[0] // TILE_SIZE)
        y = int(center[1] // TILE_SIZE)
        return (x,y)

    def _move(self, dt, direction, vector_d, board: Board, bombs: list[Bomb]) -> bool:
        """Attempt to move the player in a direction while respecting collisions and alignment.

        Args:
            dt: Time elapsed since the previous frame in seconds.
            direction: Requested movement direction.
            vector_d: Direction vector as (dx, dy).
            board: Game board used for wall collision checks.
            bombs: Currently placed bombs.

        Returns:
            bool: True if the player successfully moves.
        """
        if (direction == "RIGHT" or direction == "LEFT"):
            aligned_y = self._aligned_y()
            if self._is_inside_margin(aligned_y, self.y) and board._is_horizontal_rail(self.y):
                desired_x = self.x + vector_d[0] * self.speed * dt
                desired_y = aligned_y
                if board.can_occupy(desired_x, desired_y, PLAYER_SIZE, PLAYER_SIZE):
                    if self._can_move_through_bombs(desired_x, desired_y, bombs):
                        self.x = desired_x
                        self.y = desired_y
                        return True
        if (direction == "UP" or direction == "DOWN"):
            aligned_x = self._aligned_x()
            if self._is_inside_margin(aligned_x, self.x) and board._is_vertical_rail(self.x):
                desired_x = aligned_x
                desired_y = self.y + vector_d[1] * self.speed * dt
                if board.can_occupy(desired_x, desired_y, PLAYER_SIZE, PLAYER_SIZE):
                    if self._can_move_through_bombs(desired_x, desired_y, bombs):
                        self.x = desired_x
                        self.y = desired_y
                        return True
        return False


    def update(self, dt, pressed_directions, board: Board, bombs: list[Bomb]) -> None:
        """Update the player's movement based on pressed directions.

        Args:
            dt: Time elapsed since the previous frame in seconds.
            pressed_directions: List of currently pressed movement directions.
            board: Game board used for collision checks.
            bombs: Currently placed bombs.
        """
        if pressed_directions:
            desire_direction = pressed_directions[-1]
            vector_direction = DIRECTIONS[desire_direction]
            can_move = self._move(dt, desire_direction, vector_direction, board, bombs)

            if can_move:
                self.current_direction = desire_direction
            else:
                if self.current_direction in pressed_directions:
                    vector_direction = DIRECTIONS[self.current_direction]

                    can_move = self._move(dt, self.current_direction, vector_direction, board, bombs)


    def draw(self, screen, surfaces) -> None:
        """Draw the player using its assigned color or red if defeated.

        Args:
            screen: Pygame surface on which to draw the player.
            color: Player's assigned color.
        """
        direction = self.current_direction or "DOWN"
        offset = (TILE_SIZE - PLAYER_SIZE) / 2
        if self.alive:
            screen.blit(surfaces[direction], (self.x - offset, self.y - offset))
        else:
            screen.blit(surfaces["END"], (self.x - offset, self.y - offset))
            
            



    def apply_powerup(self, power_up: PowerUp) -> None:
        """Apply the collected power-up effect to the player.

        Args:
            power_up: Type of power-up collected.
        """
        match power_up:
            case PowerUp.BOMB_UP:
                self.max_bombs +=1
            case PowerUp.FIRE_UP:
                self.fire_power +=1
            case PowerUp.SPEED_UP:
                self.speed = min(self.speed + SPEED_UP_INCREMENT, MAX_PLAYER_SPEED)
