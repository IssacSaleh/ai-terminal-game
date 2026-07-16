# Our terminal game! A 5x5 grid with WASD movement and collectibles.

import random

# --- Player Position ---
# We use (row, col) to track where the player is on the grid.
# (0, 0) is the top-left corner.
player_row: int = 0
player_col: int = 0

# --- Collectible Position ---
collectible_row: int = 0
collectible_col: int = 0

# --- Score ---
score: int = 0
WIN_SCORE: int = 10

# --- Grid Settings ---
GRID_SIZE: int = 5


def spawn_collectible() -> None:
    """Place the collectible at a random position that isn't the player."""
    global collectible_row, collectible_col
    while True:
        collectible_row = random.randint(0, GRID_SIZE - 1)
        collectible_col = random.randint(0, GRID_SIZE - 1)
        if collectible_row != player_row or collectible_col != player_col:
            break  # Found a spot that isn't the player


def draw_grid() -> None:
    """Draws the grid to the terminal, showing the player and collectible."""
    for row in range(GRID_SIZE):
        row_string: str = ""
        for col in range(GRID_SIZE):
            if row == player_row and col == player_col:
                row_string += " P "  # Player is here!
            elif row == collectible_row and col == collectible_col:
                row_string += " C "  # Collectible is here!
            else:
                row_string += " . "  # Empty cell
            if col < GRID_SIZE - 1:
                row_string += "|"  # Column separator
        print(row_string)
        if row < GRID_SIZE - 1:
            print("-" * (GRID_SIZE * 4 - 1))


def move_player(direction: str) -> None:
    """Moves the player in the given direction, if within grid boundaries."""
    global player_row, player_col

    if direction == "w" and player_row > 0:
        player_row -= 1  # Up
    elif direction == "s" and player_row < GRID_SIZE - 1:
        player_row += 1  # Down
    elif direction == "a" and player_col > 0:
        player_col -= 1  # Left
    elif direction == "d" and player_col < GRID_SIZE - 1:
        player_col += 1  # Right


def check_collect() -> bool:
    """Check if the player is on the collectible. Score and respawn if so."""
    global score
    if player_row == collectible_row and player_col == collectible_col:
        score += 1
        spawn_collectible()
        return True
    return False


def clear_screen() -> None:
    """Clears the terminal screen."""
    print("\033c", end="")


def main() -> None:
    """Main game loop."""
    spawn_collectible()

    print("Welcome to the Grid Game!")
    print("You are 'P'. Collect the 'C' items!")
    print(f"Collect {WIN_SCORE} items to win. WASD to move.")
    input("\nPress Enter to start...")

    while True:
        clear_screen()
        print(f"Score: {score} / {WIN_SCORE}")
        draw_grid()

        user_input: str = input("\nMove (WASD) or 'quit': ").strip().lower()

        if user_input == "quit":
            print("Thanks for playing!")
            break

        if user_input in ("w", "a", "s", "d"):
            move_player(user_input)
            check_collect()

            if score >= WIN_SCORE:
                clear_screen()
                print(f"Score: {score} / {WIN_SCORE}")
                draw_grid()
                print(f"\nYou win! Final score: {score}")
                break


if __name__ == "__main__":
    main()
