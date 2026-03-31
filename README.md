# Simple Flask App with SQLite

This example app stores small notes about Python syntax.

## Install

```bash
uv sync
```

## Run

```bash
uv run flask --app app run --debug
```

Then open `http://127.0.0.1:5000` in your browser.

## What the app does

- Save Python syntax
- Save a simple explanation for it
- Read entries from a SQLite database
- Delete entries

## Important files

- `app.py`: Flask app and SQL statements
- `templates/index.html`: user interface
- `pyproject.toml`: project file with dependencies
- `syntax_notes.db`: SQLite database, created automatically
