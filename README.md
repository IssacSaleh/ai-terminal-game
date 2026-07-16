# Lia Danger Dragon

A terminal-based grid game built with Python. Navigate the dragon rider 🐉 across a 5x5 grid to collect boxes 📦 while avoiding volcanic hazards 🌋.

## Story

> *Navigate the dragon Rider to collect boxes. Be careful of fire.*

You are a dragon rider on a dangerous mission. Collect 10 boxes scattered across the grid to achieve victory — but watch out for the volcano lurking somewhere on the field. One wrong step into the fire, and it's game over.

## Features

- **WASD Movement** — intuitive keyboard controls (W=up, A=left, S=down, D=right)
- **5x5 Grid** — clean terminal-rendered grid with consistent emoji alignment
- **Collectibles** — randomised box placement that respawns after each collection
- **Hazards** — a volcano placed at a random position; step on it and you lose
- **Scoring System** — tracks your progress toward the win condition
- **Win/Lose Conditions** — collect 10 boxes to win, or hit the volcano to lose
- **Play Again** — after each game, choose to restart or exit cleanly
- **Themed Assets** — custom emojis and messages for an immersive experience

## How to Run

### Prerequisites

- Python 3.10 or higher
- A terminal that supports Unicode emojis

### Start the Game

```bash
python game.py
```

### Run the Tests

```bash
python -m pytest test_game.py -v
```

The test suite includes **46 tests** covering:

| Test Suite | Coverage |
|---|---|
| `TestTheme` | Game name, story intro, emojis, win/lose messages |
| `TestCellContent` | Cell formatting and alignment |
| `TestRandomFreeCell` | Random spawning logic and collision avoidance |
| `TestNewGame` | Game setup and position validation |
| `TestDrawGrid` | Grid rendering, emoji display, and priority rules |
| `TestMovement` | WASD controls and sequential moves |
| `TestBoundaries` | Edge detection on all four sides |
| `TestPlayGame` | Full game flow with mocked input (win, lose, quit) |
| `TestClearScreen` | Terminal reset functionality |

## Project Structure

```
ai-terminal-game/
├── game.py           # Main game logic and entry point
├── test_game.py      # Pytest test suite (46 tests)
└── README.md         # This file
```

## Architecture

The game uses a two-level loop design:

- **`main()`** — outer loop managing the title screen and play-again prompt
- **`play_game()`** — inner loop running one complete game session

All game state is passed as function parameters and return values — no global variables are mutated. This makes the code modular, testable, and easy to extend.

## What I Learned

- **Iterative Development** — built the game incrementally: grid first, then movement, collectibles, hazards, theming. Each feature was tested before moving to the next.

- **Engineering Prompts to Prevent Regression** — each new feature was accompanied by new pytest tests. When refactoring the codebase (e.g., removing globals, adding play-again), the existing tests caught breaking changes immediately.

- **Automated Testing with Pytest** — used fixtures (`autouse` reset), parametrised tests, and `monkeypatch` to mock user input. This allowed testing the full game loop without a human at the keyboard.

- **Clean Code Principles** — functions take parameters and return values instead of relying on global state. Each function has a single responsibility, making the code readable and maintainable.

## Controls

| Key | Action |
|-----|--------|
| `W` | Move up |
| `A` | Move left |
| `S` | Move down |
| `D` | Move right |
| `quit` | Exit the game |

## License

This project was built as part of a learning exercise with Correlation One.
