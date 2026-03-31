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


# Step 1: Add a helper function for the list page.
# This avoids repeating the same SELECT query in different routes.
def get_all_notes():
    conn = get_db_connection()
    notes = conn.execute(
        "SELECT id, syntax, explanation FROM syntax_notes ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return notes


# Step 2: Add a small helper function that loads one note by its id.
# We will use it when we open the edit form and when we save changes.
def get_note_by_id(note_id):
    conn = get_db_connection()
    note = conn.execute(
        "SELECT id, syntax, explanation FROM syntax_notes WHERE id = ?",
        (note_id,),
    ).fetchone()
    conn.close()
    return note


# Step 3: Add a helper that renders the page in one place.
# The page can either show an empty create form or a filled edit form.
def render_notes_page(note_to_edit=None):
    return render_template(
        "index.html",
        notes=get_all_notes(),
        note_to_edit=note_to_edit,
    )


@app.route("/")
def index():
    return render_notes_page()


# Step 4: Use CRUD language for creating a new note.
# "create" is clearer than "add" because it matches common backend naming.
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


# Step 5: Use resource-style routes for the rest of CRUD actions.
# Each route clearly shows that it works on one note by its id.
@app.get("/notes/<int:note_id>/edit")
def edit_note(note_id):
    note_to_edit = get_note_by_id(note_id)

    if note_to_edit is None:
        return redirect(url_for("index"))

    return render_notes_page(note_to_edit=note_to_edit)


# Step 6: Keep the update route explicit and close to the SQL UPDATE statement.
# It reads the changed form data and updates the matching database row.
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
