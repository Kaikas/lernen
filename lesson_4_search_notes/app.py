import sqlite3
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
DATABASE = Path(__file__).with_name("syntax_notes.db")


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS syntax_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            syntax TEXT NOT NULL,
            explanation TEXT NOT NULL
        )
        """
    )

    count = conn.execute("SELECT COUNT(*) FROM syntax_notes").fetchone()[0]

    if count == 0:
        examples = [
            ("print('Hello')", "Prints text to the console."),
            ("for number in range(3):", "Repeats a block of code 3 times."),
            ("if x > 10:", "Runs code only if the condition is true."),
        ]
        conn.executemany(
            "INSERT INTO syntax_notes (syntax, explanation) VALUES (?, ?)",
            examples,
        )

    conn.commit()
    conn.close()


def get_note_by_id(note_id):
    conn = get_db_connection()
    note = conn.execute(
        "SELECT id, syntax, explanation FROM syntax_notes WHERE id = ?",
        (note_id,),
    ).fetchone()
    conn.close()
    return note


# Step 1: Add a helper that can return all notes or only matching notes.
# This keeps the search SQL in one place instead of repeating it in multiple routes.
def get_notes(search_query=""):
    conn = get_db_connection()

    if search_query:
        pattern = f"%{search_query}%"
        notes = conn.execute(
            """
            SELECT id, syntax, explanation
            FROM syntax_notes
            WHERE syntax LIKE ? OR explanation LIKE ?
            ORDER BY id DESC
            """,
            (pattern, pattern),
        ).fetchall()
    else:
        notes = conn.execute(
            "SELECT id, syntax, explanation FROM syntax_notes ORDER BY id DESC"
        ).fetchall()

    conn.close()
    return notes


@app.route("/")
def index():
    # Step 2: Read the search text from the URL query string.
    # Example: /?q=loop
    search_query = request.args.get("q", "").strip()
    return render_template(
        "index.html",
        notes=get_notes(search_query),
        note_to_edit=None,
        search_query=search_query,
    )


@app.post("/notes/create")
def create_note():
    syntax = request.form["syntax"].strip()
    explanation = request.form["explanation"].strip()

    if syntax and explanation:
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO syntax_notes (syntax, explanation) VALUES (?, ?)",
            (syntax, explanation),
        )
        conn.commit()
        conn.close()

    return redirect(url_for("index"))


@app.get("/notes/<int:note_id>/edit")
def edit_note(note_id):
    note_to_edit = get_note_by_id(note_id)

    if note_to_edit is None:
        return redirect(url_for("index"))

    return render_template(
        "index.html",
        notes=get_notes(),
        note_to_edit=note_to_edit,
        search_query="",
    )


@app.post("/notes/<int:note_id>/update")
def update_note(note_id):
    syntax = request.form["syntax"].strip()
    explanation = request.form["explanation"].strip()

    if not get_note_by_id(note_id):
        return redirect(url_for("index"))

    if syntax and explanation:
        conn = get_db_connection()
        conn.execute(
            """
            UPDATE syntax_notes
            SET syntax = ?, explanation = ?
            WHERE id = ?
            """,
            (syntax, explanation, note_id),
        )
        conn.commit()
        conn.close()

    return redirect(url_for("index"))


@app.get("/notes/<int:note_id>")
def show_note(note_id):
    note = get_note_by_id(note_id)

    if note is None:
        return redirect(url_for("index"))

    return render_template("detail.html", note=note)


@app.post("/notes/<int:note_id>/delete")
def delete_note(note_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM syntax_notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


init_db()


if __name__ == "__main__":
    app.run(debug=True)
