# Repository Guidelines

## Project Structure & Module Organization
This project uses a `src` layout. Core package code lives in `src/qfinancetools/`.
- `core/`: pure financial calculations (no CLI/GUI I/O)
- `models/`: Pydantic input/output models
- `cli/`: Typer app, commands, prompts, and renderers
- `gui/`: PySide6 desktop app pages/widgets/theme
- `tests/`: pytest suite (`test_*.py`) aligned to domains (`loans`, `bonds`, `risk`, etc.)

Keep business logic in `core` and call it from thin CLI/GUI layers.

## Build, Test, and Development Commands
Use `uv` for environment and execution.
- `uv venv && source .venv/bin/activate`: create and activate local virtualenv
- `uv sync`: install dependencies from `pyproject.toml`/`uv.lock`
- `uv run qfin --help`: run CLI entrypoint
- `uv run qfin-gui`: launch desktop GUI
- `uv run pytest`: run tests (`-q` is enabled by pytest config)
- `ruff check --fix . && ruff format .`: lint and format (project convention)

## Coding Style & Naming Conventions
- Target: Python 3.11+; prefer type hints on public functions
- Indentation: 4 spaces; follow PEP 8 defaults
- Naming: `snake_case` for modules/functions/variables, `PascalCase` for models/classes
- Keep functions deterministic in `core`; validate interfaces through Pydantic models in `models`
- CLI commands should remain small wrappers around `core` APIs

## Testing Guidelines
- Frameworks: `pytest` with `hypothesis` for property-based coverage where useful
- File naming: `tests/test_<domain>.py`; test names like `test_<behavior>()`
- Add regression tests for financial edge cases (zero rates, invalid periods, extreme inputs)
- Run `uv run pytest` before opening a PR

## Commit & Pull Request Guidelines
Recent history favors short, imperative commit subjects (for example, `Add GUI entrypoint and Monte Carlo values output`).
- Commits: one logical change per commit; concise subject line
- PRs should include: what changed, why, and test evidence (`uv run pytest` output summary)
- Link related issues and include screenshots for GUI changes
- Note breaking CLI/UI changes explicitly in the PR description
