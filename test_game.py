"""Pytest tests for game.py — themed game with play-again."""

import io
import sys
from typing import Generator

import pytest

import game
from game import (
    draw_grid,
    move_player,
    clear_screen,
    new_game,
    play_game,
    _random_free_cell,
    _cell_content,
    GRID_SIZE,
    WIN_SCORE,
    PLAYER,
    COLLECTIBLE,
    HAZARD,
    GAME_NAME,
    STORY_INTRO,
    WIN_MSG,
    LOSE_MSG,
)


# ---------------------------------------------------------------------------
# Helper: capture what draw_grid() prints to stdout
# ---------------------------------------------------------------------------
def capture_grid(
    pr: int, pc: int, cr: int, cc: int, hr: int, hc: int
) -> str:
    buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf
    draw_grid(pr, pc, cr, cc, hr, hc)
    sys.stdout = old_stdout
    return buf.getvalue()


# ============================== THEME CONSTANTS ==============================

class TestTheme:
    """Tests for the custom theme assets."""

    def test_game_name(self) -> None:
        assert GAME_NAME == "[Lia Danger dragon]"

    def test_story_intro(self) -> None:
        assert "dragon Rider" in STORY_INTRO
        assert "fire" in STORY_INTRO

    def test_player_emoji(self) -> None:
        assert PLAYER == "🐉"

    def test_collectible_emoji(self) -> None:
        assert COLLECTIBLE == "📦"

    def test_hazard_emoji(self) -> None:
        assert HAZARD == "🌋"

    def test_win_message(self) -> None:
        assert WIN_MSG == "[Victooooory!!!]"

    def test_lose_message(self) -> None:
        assert LOSE_MSG == "[ You lose!!! ]"


# ============================== CELL CONTENT =================================

class TestCellContent:
    """Tests for the _cell_content() helper."""

    def test_empty_cell(self) -> None:
        result = _cell_content(" ")
        assert result.center(4) == result  # should be centred in 4 cols

    def test_emoji_cell(self) -> None:
        result = _cell_content(PLAYER)
        assert PLAYER in result
        assert result.startswith(" ")
        assert result.endswith(" ")


# ============================== RANDOM FREE CELL ============================

class TestRandomFreeCell:
    """Tests for the _random_free_cell() helper."""

    def test_within_grid(self) -> None:
        for _ in range(100):
            r, c = _random_free_cell(0, 0, -1, -1)
            assert 0 <= r < GRID_SIZE
            assert 0 <= c < GRID_SIZE

    def test_avoids_single_position(self) -> None:
        for _ in range(100):
            r, c = _random_free_cell(2, 2, -1, -1)
            assert (r, c) != (2, 2)

    def test_avoids_two_positions(self) -> None:
        for _ in range(100):
            r, c = _random_free_cell(0, 0, 4, 4)
            assert (r, c) != (0, 0)
            assert (r, c) != (4, 4)

    def test_ignores_negative_sentinel(self) -> None:
        results = set()
        for _ in range(200):
            r, c = _random_free_cell(2, 2, -1, -1)
            results.add((r, c))
        assert len(results) > 1


# ============================== NEW GAME =====================================

class TestNewGame:
    """Tests for the new_game() setup function."""

    def test_returns_six_integers(self) -> None:
        result = new_game()
        assert len(result) == 6
        assert all(isinstance(v, int) for v in result)

    def test_player_starts_at_origin(self) -> None:
        pr, pc, *_ = new_game()
        assert pr == 0
        assert pc == 0

    def test_all_positions_in_bounds(self) -> None:
        for _ in range(100):
            pr, pc, cr, cc, hr, hc = new_game()
            for pos in (pr, pc, cr, cc, hr, hc):
                assert 0 <= pos < GRID_SIZE

    def test_collectible_not_on_player(self) -> None:
        for _ in range(100):
            pr, pc, cr, cc, *_ = new_game()
            assert (cr, cc) != (pr, pc)

    def test_hazard_not_on_player(self) -> None:
        for _ in range(100):
            pr, pc, _, _, hr, hc = new_game()
            assert (hr, hc) != (pr, pc)

    def test_hazard_not_on_collectible(self) -> None:
        for _ in range(100):
            _, _, cr, cc, hr, hc = new_game()
            assert (hr, hc) != (cr, cc)


# ============================== GRID DRAWING ===============================

class TestDrawGrid:
    """Tests for the draw_grid() function."""

    def test_player_shown_at_origin(self) -> None:
        grid = capture_grid(0, 0, 3, 3, 4, 4)
        assert PLAYER in grid.splitlines()[0]

    def test_player_shown_at_center(self) -> None:
        grid = capture_grid(2, 2, 0, 0, 4, 4)
        assert PLAYER in grid.splitlines()[4]

    def test_player_shown_at_bottom_right(self) -> None:
        grid = capture_grid(4, 4, 0, 0, 2, 2)
        assert PLAYER in grid.splitlines()[-1]

    def test_grid_has_correct_number_of_rows(self) -> None:
        grid = capture_grid(0, 0, 3, 3, 4, 4)
        assert len(grid.splitlines()) == GRID_SIZE * 2 - 1

    def test_grid_contains_separator_lines(self) -> None:
        lines = capture_grid(0, 0, 3, 3, 4, 4).splitlines()
        for i in range(1, len(lines), 2):
            assert all(ch == "-" for ch in lines[i])

    def test_empty_cells_are_blank(self) -> None:
        grid = capture_grid(0, 0, 4, 4, 4, 0)
        line = grid.splitlines()[2]  # row 1 — empty
        assert PLAYER not in line
        assert COLLECTIBLE not in line
        assert HAZARD not in line

    def test_collectible_shown(self) -> None:
        grid = capture_grid(0, 0, 2, 2, 4, 4)
        assert COLLECTIBLE in grid.splitlines()[4]

    def test_hazard_shown(self) -> None:
        grid = capture_grid(0, 0, 4, 4, 1, 1)
        assert HAZARD in grid.splitlines()[2]

    def test_player_priority_over_collectible(self) -> None:
        grid = capture_grid(1, 1, 1, 1, 4, 4)
        line = grid.splitlines()[2]
        assert PLAYER in line
        assert COLLECTIBLE not in line

    def test_player_priority_over_hazard(self) -> None:
        grid = capture_grid(1, 1, 4, 4, 1, 1)
        line = grid.splitlines()[2]
        assert PLAYER in line
        assert HAZARD not in line

    def test_hazard_priority_over_collectible(self) -> None:
        grid = capture_grid(0, 0, 2, 2, 2, 2)
        line = grid.splitlines()[4]
        assert HAZARD in line
        assert COLLECTIBLE not in line


# ============================== MOVEMENT ====================================

class TestMovement:
    """Tests for the move_player() function."""

    def test_move_right(self) -> None:
        r, c = move_player("d", 0, 0)
        assert r == 0 and c == 1

    def test_move_left(self) -> None:
        r, c = move_player("a", 0, 2)
        assert r == 0 and c == 1

    def test_move_down(self) -> None:
        r, c = move_player("s", 0, 0)
        assert r == 1 and c == 0

    def test_move_up(self) -> None:
        r, c = move_player("w", 2, 0)
        assert r == 1 and c == 0

    def test_sequential_moves(self) -> None:
        r, c = move_player("d", 0, 0)
        r, c = move_player("s", r, c)
        r, c = move_player("d", r, c)
        r, c = move_player("w", r, c)
        assert r == 0 and c == 2

    def test_full_perimeter_walk(self) -> None:
        r, c = 0, 0
        for _ in range(GRID_SIZE - 1):
            r, c = move_player("d", r, c)
        for _ in range(GRID_SIZE - 1):
            r, c = move_player("s", r, c)
        for _ in range(GRID_SIZE - 1):
            r, c = move_player("a", r, c)
        for _ in range(GRID_SIZE - 1):
            r, c = move_player("w", r, c)
        assert r == 0 and c == 0


# ============================== BOUNDARIES ==================================

class TestBoundaries:
    """Tests that the player cannot move outside the grid."""

    @pytest.mark.parametrize("direction, start_r, start_c, expected_r, expected_c", [
        ("w", 0, 2, 0, 2),
        ("s", GRID_SIZE - 1, 2, GRID_SIZE - 1, 2),
        ("a", 2, 0, 2, 0),
        ("d", 2, GRID_SIZE - 1, 2, GRID_SIZE - 1),
    ])
    def test_boundary_blocks_movement(
        self,
        direction: str,
        start_r: int,
        start_c: int,
        expected_r: int,
        expected_c: int,
    ) -> None:
        r, c = move_player(direction, start_r, start_c)
        assert r == expected_r and c == expected_c


# ============================== PLAY GAME ===================================

class TestPlayGame:
    """Tests for the play_game() function via input mocking."""

    def test_quit_returns_quit(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr("builtins.input", lambda _: "quit")
        assert play_game() == "quit"

    def test_hazard_returns_lose(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Move right twice: (0,0) -> (0,1) -> (0,2). Place hazard at (0,2)."""
        inputs = iter(["d", "d"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        def fake_new_game() -> tuple[int, int, int, int, int, int]:
            return 0, 0, 4, 4, 0, 2  # hazard at (0,2)
        monkeypatch.setattr(game, "new_game", fake_new_game)
        assert play_game() == "lose"

    def test_win_returns_win(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Simulate collecting 10 items by alternating d/a to re-collect."""
        def fake_new_game() -> tuple[int, int, int, int, int, int]:
            return 0, 0, 0, 1, 4, 4  # collectible at (0,1)

        def fake_random_free_cell(
            r1: int, c1: int, r2: int, c2: int
        ) -> tuple[int, int]:
            return 0, 1  # always respawn collectible at (0,1)

        monkeypatch.setattr(game, "new_game", fake_new_game)
        monkeypatch.setattr(game, "_random_free_cell", fake_random_free_cell)

        moves: list[str] = []
        for i in range(10):
            moves.append("d")  # collect
            if i < 9:
                moves.append("a")  # move back to re-collect next turn
        inputs = iter(moves)
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        assert play_game() == "win"


# ============================== CLEAR SCREEN ================================

class TestClearScreen:
    """Tests for the clear_screen() function."""

    def test_clear_screen_outputs_escape_sequence(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        clear_screen()
        captured = capsys.readouterr()
        assert "\033c" in captured.out


# ============================== GAME CONSTANTS ==============================

class TestConstants:
    """Tests for game constants."""

    def test_win_score(self) -> None:
        assert WIN_SCORE == 10

    def test_grid_size(self) -> None:
        assert GRID_SIZE == 5
