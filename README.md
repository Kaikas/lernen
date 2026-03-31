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

- Create Python syntax notes
- Read notes from a SQLite database
- Update existing entries
- Delete entries

## Learning note

The CRUD structure and the edit feature are explained directly in the code with numbered comments.
Follow the `Step 1`, `Step 2`, and later comments to learn the change piece by piece.

## Important files

- `app.py`: Flask app and SQL statements
- `templates/index.html`: user interface
- `pyproject.toml`: project file with dependencies
- `syntax_notes.db`: SQLite database, created automatically
