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


SORT_OPTIONS = {
    "newest": "id DESC",
    "oldest": "id ASC",
    "syntax": "syntax ASC",
}


def get_notes(search_query="", sort_query="newest"):
    conn = get_db_connection()
    order_by = SORT_OPTIONS.get(sort_query, SORT_OPTIONS["newest"])
    params = []
    sql = "SELECT id, syntax, explanation FROM syntax_notes"

    if search_query:
        sql += " WHERE syntax LIKE ? OR explanation LIKE ?"
        pattern = f"%{search_query}%"
        params.extend([pattern, pattern])

    sql += f" ORDER BY {order_by}"
    notes = conn.execute(sql, params).fetchall()
    conn.close()
    return notes


# Step 1: Add one helper that renders the page with optional errors.
# This makes it easier to reuse the same template after invalid input.
def render_index_page(
    note_to_edit=None,
    error_message="",
    form_data=None,
    search_query="",
    sort_query="newest",
):
    return render_template(
        "index.html",
        notes=get_notes(search_query, sort_query),
        note_to_edit=note_to_edit,
        error_message=error_message,
        form_data=form_data or {},
        search_query=search_query,
        sort_query=sort_query,
    )


@app.route("/")
def index():
    search_query = request.args.get("q", "").strip()
    sort_query = request.args.get("sort", "newest")
    return render_index_page(
        search_query=search_query,
        sort_query=sort_query,
    )


@app.post("/notes/create")
def create_note():
    syntax = request.form["syntax"].strip()
    explanation = request.form["explanation"].strip()

    # Step 2: Show a clear validation error instead of silently ignoring invalid input.
    if not syntax or not explanation:
        return (
            render_index_page(
                error_message="Both fields are required.",
                form_data={"syntax": syntax, "explanation": explanation},
            ),
            400,
        )

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

    return render_index_page(note_to_edit=note_to_edit)


@app.post("/notes/<int:note_id>/update")
def update_note(note_id):
    syntax = request.form["syntax"].strip()
    explanation = request.form["explanation"].strip()
    note_to_edit = get_note_by_id(note_id)

    if note_to_edit is None:
        return redirect(url_for("index"))

    # Step 3: Apply the same validation rules to updates.
    if not syntax or not explanation:
        return (
            render_index_page(
                note_to_edit=note_to_edit,
                error_message="Both fields are required.",
                form_data={"syntax": syntax, "explanation": explanation},
            ),
            400,
        )

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
