"""Pytest tests for game.py — grid drawing, movement, and boundaries."""

import io
import sys
from typing import Generator

import pytest

import game
from game import draw_grid, move_player, clear_screen, GRID_SIZE


# ---------------------------------------------------------------------------
# Fixture: reset player to (0, 0) before every test so tests don't interfere
# with each other.
# ---------------------------------------------------------------------------
@pytest.fixture(autouse=True)
def reset_player() -> Generator[None, None, None]:
    """Reset player position to (0, 0) before each test."""
    game.player_row = 0
    game.player_col = 0
    yield
    # Cleanup (optional reset after test too)
    game.player_row = 0
    game.player_col = 0


# ---------------------------------------------------------------------------
# Helper: capture what draw_grid() prints to stdout
# ---------------------------------------------------------------------------
def capture_grid() -> str:
    buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf
    draw_grid()
    sys.stdout = old_stdout
    return buf.getvalue()


# ============================== GRID DRAWING ===============================

class TestDrawGrid:
    """Tests for the draw_grid() function."""

    def test_player_shown_at_origin(self) -> None:
        """Grid should show P in the top-left cell when player is at (0,0)."""
        lines = capture_grid().splitlines()
        assert "P" in lines[0]

    def test_player_shown_at_center(self) -> None:
        """Grid should show P on the correct row when player is at (2,2)."""
        game.player_row = 2
        game.player_col = 2
        lines = capture_grid().splitlines()
        # Row 0 = line 0, separator = line 1, Row 1 = line 2, separator = line 3,
        # Row 2 = line 4
        assert "P" in lines[4]

    def test_player_shown_at_bottom_right(self) -> None:
        """Grid should show P in the bottom-right cell at (4,4)."""
        game.player_row = 4
        game.player_col = 4
        lines = capture_grid().splitlines()
        # Row 4 = last row line
        assert "P" in lines[-1]

    def test_grid_has_correct_number_of_rows(self) -> None:
        """Grid should have 9 lines: 5 data rows + 4 separators."""
        lines = capture_grid().splitlines()
        assert len(lines) == GRID_SIZE * 2 - 1

    def test_grid_contains_separator_lines(self) -> None:
        """Odd-indexed lines should be dashes (separators)."""
        lines = capture_grid().splitlines()
        for i in range(1, len(lines), 2):
            assert all(ch == "-" for ch in lines[i])

    def test_empty_cells_show_dot(self) -> None:
        """Cells without the player should display '.'."""
        game.player_row = 0
        game.player_col = 0
        lines = capture_grid().splitlines()
        # Line 2 is row 1 — player is NOT on row 1
        assert "P" not in lines[2]
        assert "." in lines[2]


# ============================== MOVEMENT ====================================

class TestMovement:
    """Tests for the move_player() function."""

    def test_move_right(self) -> None:
        move_player("d")
        assert game.player_row == 0
        assert game.player_col == 1

    def test_move_left(self) -> None:
        game.player_col = 2
        move_player("a")
        assert game.player_row == 0
        assert game.player_col == 1

    def test_move_down(self) -> None:
        move_player("s")
        assert game.player_row == 1
        assert game.player_col == 0

    def test_move_up(self) -> None:
        game.player_row = 2
        move_player("w")
        assert game.player_row == 1
        assert game.player_col == 0

    def test_sequential_moves(self) -> None:
        """Multiple moves should chain correctly."""
        move_player("d")  # -> (0, 1)
        move_player("s")  # -> (1, 1)
        move_player("d")  # -> (1, 2)
        move_player("w")  # -> (0, 2)
        assert game.player_row == 0
        assert game.player_col == 2

    def test_full_perimeter_walk(self) -> None:
        """Walk around the entire border and return to start."""
        for _ in range(GRID_SIZE - 1):
            move_player("d")
        for _ in range(GRID_SIZE - 1):
            move_player("s")
        for _ in range(GRID_SIZE - 1):
            move_player("a")
        for _ in range(GRID_SIZE - 1):
            move_player("w")
        assert game.player_row == 0
        assert game.player_col == 0


# ============================== BOUNDARIES ==================================

class TestBoundaries:
    """Tests that the player cannot move outside the grid."""

    def test_cannot_move_above_top(self) -> None:
        game.player_row = 0
        move_player("w")
        assert game.player_row == 0

    def test_cannot_move_below_bottom(self) -> None:
        game.player_row = GRID_SIZE - 1
        move_player("s")
        assert game.player_row == GRID_SIZE - 1

    def test_cannot_move_past_left(self) -> None:
        game.player_col = 0
        move_player("a")
        assert game.player_col == 0

    def test_cannot_move_past_right(self) -> None:
        game.player_col = GRID_SIZE - 1
        move_player("d")
        assert game.player_col == GRID_SIZE - 1

    @pytest.mark.parametrize("direction, start_row, start_col", [
        ("w", 0, 2),  # top edge
        ("s", GRID_SIZE - 1, 2),  # bottom edge
        ("a", 2, 0),  # left edge
        ("d", 2, GRID_SIZE - 1),  # right edge
    ])
    def test_boundary_parametrized(
        self, direction: str, start_row: int, start_col: int
    ) -> None:
        """Each edge should block movement in the corresponding direction."""
        game.player_row = start_row
        game.player_col = start_col
        move_player(direction)
        assert game.player_row == start_row
        assert game.player_col == start_col


# ============================== CLEAR SCREEN ================================

class TestClearScreen:
    """Tests for the clear_screen() function."""

    def test_clear_screen_outputs_escape_sequence(self, capsys: pytest.CaptureFixture[str]) -> None:
        """clear_screen() should print the terminal reset escape sequence."""
        clear_screen()
        captured = capsys.readouterr()
        assert "\033c" in captured.out


# ============================== INVALID INPUT ================================

class TestInvalidInput:
    """Tests that invalid directions are safely ignored."""

    @pytest.mark.parametrize("bad_input", ["x", "q", "wasd", "", "1", "W"])
    def test_invalid_direction_does_not_move(self, bad_input: str) -> None:
        move_player(bad_input)
        assert game.player_row == 0
        assert game.player_col == 0
