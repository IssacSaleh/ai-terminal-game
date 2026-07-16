"""Pytest tests for game.py — grid, movement, boundaries, collectibles, hazards."""

import io
import sys
from typing import Generator

import pytest

import game
from game import (
    draw_grid,
    move_player,
    clear_screen,
    spawn_collectible,
    spawn_hazard,
    check_collect,
    check_hazard,
    GRID_SIZE,
    WIN_SCORE,
)


# ---------------------------------------------------------------------------
# Fixture: reset all game state before every test.
# ---------------------------------------------------------------------------
@pytest.fixture(autouse=True)
def reset_game() -> Generator[None, None, None]:
    """Reset player, collectible, hazard, and score before each test."""
    game.player_row = 0
    game.player_col = 0
    game.collectible_row = 3
    game.collectible_col = 3
    game.hazard_row = 4
    game.hazard_col = 4
    game.score = 0
    yield
    game.player_row = 0
    game.player_col = 0
    game.score = 0


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
        assert "P" in lines[4]

    def test_player_shown_at_bottom_right(self) -> None:
        """Grid should show P in the bottom-right cell at (4,4)."""
        game.player_row = 4
        game.player_col = 4
        lines = capture_grid().splitlines()
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
        """Cells without player, collectible, or hazard should display '.'."""
        game.player_row = 0
        game.player_col = 0
        game.collectible_row = 4
        game.collectible_col = 4
        game.hazard_row = 4
        game.hazard_col = 0
        lines = capture_grid().splitlines()
        # Line 2 is row 1 — nothing is on row 1
        assert "P" not in lines[2]
        assert "C" not in lines[2]
        assert "X" not in lines[2]
        assert "." in lines[2]

    def test_collectible_shown_on_grid(self) -> None:
        """Grid should show C where the collectible is placed."""
        game.collectible_row = 2
        game.collectible_col = 2
        lines = capture_grid().splitlines()
        assert "C" in lines[4]

    def test_hazard_shown_on_grid(self) -> None:
        """Grid should show X where the hazard is placed."""
        game.hazard_row = 1
        game.hazard_col = 1
        lines = capture_grid().splitlines()
        assert "X" in lines[2]  # Row 1 = line 2

    def test_player_takes_priority_over_collectible(self) -> None:
        """If player and collectible are on the same cell, show P not C."""
        game.player_row = 1
        game.player_col = 1
        game.collectible_row = 1
        game.collectible_col = 1
        lines = capture_grid().splitlines()
        assert "P" in lines[2]
        assert "C" not in lines[2]

    def test_player_takes_priority_over_hazard(self) -> None:
        """If player and hazard are on the same cell, show P not X."""
        game.player_row = 1
        game.player_col = 1
        game.hazard_row = 1
        game.hazard_col = 1
        lines = capture_grid().splitlines()
        assert "P" in lines[2]
        assert "X" not in lines[2]

    def test_hazard_takes_priority_over_collectible(self) -> None:
        """If hazard and collectible share a cell, show X not C."""
        game.hazard_row = 2
        game.hazard_col = 2
        game.collectible_row = 2
        game.collectible_col = 2
        lines = capture_grid().splitlines()
        assert "X" in lines[4]
        assert "C" not in lines[4]


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
        ("w", 0, 2),
        ("s", GRID_SIZE - 1, 2),
        ("a", 2, 0),
        ("d", 2, GRID_SIZE - 1),
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


# ============================== COLLECTIBLE SPAWNING ========================

class TestSpawnCollectible:
    """Tests for the spawn_collectible() function."""

    def test_collectible_within_grid(self) -> None:
        """Collectible should always be inside the grid boundaries."""
        for _ in range(100):
            spawn_collectible()
            assert 0 <= game.collectible_row < GRID_SIZE
            assert 0 <= game.collectible_col < GRID_SIZE

    def test_collectible_not_on_player(self) -> None:
        """Collectible should never spawn on top of the player."""
        game.player_row = 2
        game.player_col = 2
        for _ in range(100):
            spawn_collectible()
            assert (game.collectible_row, game.collectible_col) != (2, 2)

    def test_collectible_varies_position(self) -> None:
        """Over many spawns, collectible should land on different spots."""
        game.player_row = 0
        game.player_col = 0
        positions = set()
        for _ in range(200):
            spawn_collectible()
            positions.add((game.collectible_row, game.collectible_col))
        assert len(positions) > 1


# ============================== COLLECT LOGIC ================================

class TestCheckCollect:
    """Tests for the check_collect() function."""

    def test_collect_increases_score(self) -> None:
        """Walking onto the collectible should bump the score by 1."""
        game.player_row = game.collectible_row
        game.player_col = game.collectible_col
        result = check_collect()
        assert result is True
        assert game.score == 1

    def test_collect_respawns_item(self) -> None:
        """After collecting, the collectible should move to a new position."""
        old_pos = (game.collectible_row, game.collectible_col)
        game.player_row = old_pos[0]
        game.player_col = old_pos[1]
        check_collect()
        new_pos = (game.collectible_row, game.collectible_col)
        assert 0 <= new_pos[0] < GRID_SIZE
        assert 0 <= new_pos[1] < GRID_SIZE

    def test_no_collect_when_not_on_item(self) -> None:
        """Score should NOT increase if player isn't on the collectible."""
        game.collectible_row = 4
        game.collectible_col = 4
        result = check_collect()
        assert result is False
        assert game.score == 0

    def test_multiple_collections(self) -> None:
        """Collecting multiple times should increment score correctly."""
        for expected in range(1, 6):
            game.player_row = game.collectible_row
            game.player_col = game.collectible_col
            check_collect()
            assert game.score == expected


# ============================== WIN CONDITION ================================

class TestWinCondition:
    """Tests for the win condition at WIN_SCORE."""

    def test_win_score_constant(self) -> None:
        """Win score should be 10."""
        assert WIN_SCORE == 10

    def test_score_reaches_win(self) -> None:
        """Collecting WIN_SCORE times should set score to WIN_SCORE."""
        for _ in range(WIN_SCORE):
            game.player_row = game.collectible_row
            game.player_col = game.collectible_col
            check_collect()
        assert game.score == WIN_SCORE


# ============================== HAZARD SPAWNING ==============================

class TestSpawnHazard:
    """Tests for the spawn_hazard() function."""

    def test_hazard_within_grid(self) -> None:
        """Hazard should always be inside the grid boundaries."""
        for _ in range(100):
            spawn_hazard()
            assert 0 <= game.hazard_row < GRID_SIZE
            assert 0 <= game.hazard_col < GRID_SIZE

    def test_hazard_not_on_player(self) -> None:
        """Hazard should never spawn on top of the player."""
        game.player_row = 2
        game.player_col = 2
        for _ in range(100):
            spawn_hazard()
            assert (game.hazard_row, game.hazard_col) != (2, 2)

    def test_hazard_not_on_collectible(self) -> None:
        """Hazard should never spawn on top of the collectible."""
        game.collectible_row = 1
        game.collectible_col = 1
        for _ in range(100):
            spawn_hazard()
            assert (game.hazard_row, game.hazard_col) != (1, 1)

    def test_hazard_varies_position(self) -> None:
        """Over many spawns, hazard should land on different spots."""
        game.player_row = 0
        game.player_col = 0
        game.collectible_row = 4
        game.collectible_col = 4
        positions = set()
        for _ in range(200):
            spawn_hazard()
            positions.add((game.hazard_row, game.hazard_col))
        assert len(positions) > 1


# ============================== HAZARD CHECK =================================

class TestCheckHazard:
    """Tests for the check_hazard() function."""

    def test_hazard_returns_true_when_on_hazard(self) -> None:
        """Should return True when player is on the hazard."""
        game.player_row = game.hazard_row
        game.player_col = game.hazard_col
        assert check_hazard() is True

    def test_hazard_returns_false_when_safe(self) -> None:
        """Should return False when player is not on the hazard."""
        game.player_row = 0
        game.player_col = 0
        game.hazard_row = 4
        game.hazard_col = 4
        assert check_hazard() is False

    def test_hazard_at_each_corner(self) -> None:
        """Player stepping on hazard at any corner should return True."""
        corners = [(0, 0), (0, 4), (4, 0), (4, 4)]
        for hr, hc in corners:
            game.hazard_row = hr
            game.hazard_col = hc
            game.player_row = hr
            game.player_col = hc
            assert check_hazard() is True


# ============================== CLEAR SCREEN ================================

class TestClearScreen:
    """Tests for the clear_screen() function."""

    def test_clear_screen_outputs_escape_sequence(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
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
