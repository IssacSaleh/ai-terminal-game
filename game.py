# Lia Danger Dragon — A terminal grid game.

import random

# --- Theme ---
GAME_NAME: str = "[Lia Danger dragon]"
STORY_INTRO: str = "[Navigate the dragon Rider to collect boxes.Be careful of fire]"
PLAYER: str = "🐉"
COLLECTIBLE: str = "📦"
HAZARD: str = "🌋"
WIN_MSG: str = "[Victooooory!!!]"
LOSE_MSG: str = "[ You lose!!! ]"

# --- Grid Settings ---
GRID_SIZE: int = 5
WIN_SCORE: int = 10
CELL_WIDTH: int = 4  # visual width of each cell in terminal columns


def new_game() -> tuple[int, int, int, int, int, int]:
    """Set up a fresh game. Returns (player_row, player_col, collectible_row,
    collectible_col, hazard_row, hazard_col). Score always starts at 0."""
    pr, pc = 0, 0
    cr, cc = _random_free_cell(pr, pc, -1, -1)
    hr, hc = _random_free_cell(pr, pc, cr, cc)
    return pr, pc, cr, cc, hr, hc


def _random_free_cell(r1: int, c1: int, r2: int, c2: int) -> tuple[int, int]:
    """Pick a random cell that isn't occupied by (r1,c1) or (r2,c2).
    Pass -1 for r2/c2 to only avoid one position."""
    while True:
        r = random.randint(0, GRID_SIZE - 1)
        c = random.randint(0, GRID_SIZE - 1)
        if (r, c) != (r1, c1) and (r, c) != (r2, c2):
            return r, c


def _cell_content(symbol: str) -> str:
    """Format a cell with consistent width. Emojis are 2 terminal columns
    wide, so emoji cells get one space on each side. Empty cells get
    proportional padding to stay aligned."""
    if symbol == " ":
        return symbol.center(CELL_WIDTH)
    return f" {symbol} "


def draw_grid(
    pr: int, pc: int, cr: int, cc: int, hr: int, hc: int
) -> None:
    """Draw the grid showing the player, collectible, and hazard."""
    empty: str = " "
    sep_width: int = GRID_SIZE * CELL_WIDTH + (GRID_SIZE - 1)

    for row in range(GRID_SIZE):
        row_string: str = ""
        for col in range(GRID_SIZE):
            if row == pr and col == pc:
                cell = _cell_content(PLAYER)
            elif row == hr and col == hc:
                cell = _cell_content(HAZARD)
            elif row == cr and col == cc:
                cell = _cell_content(COLLECTIBLE)
            else:
                cell = _cell_content(empty)
            row_string += cell
            if col < GRID_SIZE - 1:
                row_string += "|"
        print(row_string)
        if row < GRID_SIZE - 1:
            print("-" * sep_width)


def move_player(direction: str, pr: int, pc: int) -> tuple[int, int]:
    """Move the player one cell in the given direction (if in bounds).
    Returns the new (row, col)."""
    if direction == "w" and pr > 0:
        pr -= 1
    elif direction == "s" and pr < GRID_SIZE - 1:
        pr += 1
    elif direction == "a" and pc > 0:
        pc -= 1
    elif direction == "d" and pc < GRID_SIZE - 1:
        pc += 1
    return pr, pc


def clear_screen() -> None:
    """Clear the terminal screen."""
    print("\033c", end="")


def play_game() -> str:
    """Run one full game. Returns 'win', 'lose', or 'quit'."""
    pr, pc, cr, cc, hr, hc = new_game()
    score: int = 0

    while True:
        clear_screen()
        print(f"Score: {score} / {WIN_SCORE}")
        draw_grid(pr, pc, cr, cc, hr, hc)

        user_input: str = input("\nMove (WASD) or 'quit': ").strip().lower()

        if user_input == "quit":
            return "quit"

        if user_input not in ("w", "a", "s", "d"):
            continue

        pr, pc = move_player(user_input, pr, pc)

        # --- Check hazard (game over) ---
        if pr == hr and pc == hc:
            clear_screen()
            print(f"Score: {score} / {WIN_SCORE}")
            draw_grid(pr, pc, cr, cc, hr, hc)
            print(f"\n{LOSE_MSG}")
            return "lose"

        # --- Check collectible (score up + respawn) ---
        if pr == cr and pc == cc:
            score += 1
            cr, cc = _random_free_cell(pr, pc, hr, hc)

            if score >= WIN_SCORE:
                clear_screen()
                print(f"Score: {score} / {WIN_SCORE}")
                draw_grid(pr, pc, cr, cc, hr, hc)
                print(f"\n{WIN_MSG} Final score: {score}")
                return "win"


def main() -> None:
    """Outer game loop with play-again support."""
    print(f"{'=' * 40}")
    print(f"        {GAME_NAME}")
    print(f"{'=' * 40}")
    print(f"\n{STORY_INTRO}\n")
    print(f"  You are {PLAYER}. Collect {COLLECTIBLE} items!")
    print(f"  Avoid the {HAZARD} hazard!")
    print(f"  Collect {WIN_SCORE} items to win. WASD to move.")
    input("\nPress Enter to start...")

    while True:
        result: str = play_game()

        if result == "quit":
            print("Thanks for playing!")
            break

        answer: str = input("\nPlay again? (y/n): ").strip().lower()
        if answer != "y":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
