# Our terminal game! A 5x5 grid with WASD movement.

# --- Player Position ---
# We use (row, col) to track where the player is on the grid.
# (0, 0) is the top-left corner.
player_row: int = 0
player_col: int = 0

# --- Grid Settings ---
GRID_SIZE: int = 5


def draw_grid() -> None:
    """Draws the grid to the terminal, showing the player's position."""
    for row in range(GRID_SIZE):
        # Build one row of the grid as a string
        row_string: str = ""
        for col in range(GRID_SIZE):
            if row == player_row and col == player_col:
                row_string += " P "  # Player is here!
            else:
                row_string += " . "  # Empty cell
            if col < GRID_SIZE - 1:
                row_string += "|"  # Column separator
        print(row_string)
        # Draw a horizontal line between rows (but not after the last one)
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


def clear_screen() -> None:
    """Clears the terminal screen."""
    print("\033c", end="")


def main() -> None:
    """Main game loop."""
    print("Welcome to the Grid Game!")
    print("You are 'P' on a 5x5 grid.")
    print("WASD to move, 'quit' to exit.")
    input("\nPress Enter to start...")

    while True:
        clear_screen()
        draw_grid()

        user_input: str = input("\nMove (WASD) or 'quit': ").strip().lower()

        if user_input == "quit":
            print("Thanks for playing!")
            break

        if user_input in ("w", "a", "s", "d"):
            move_player(user_input)


if __name__ == "__main__":
    main()
