import sqlite3
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
DATABASE = Path(__file__).with_name("syntax_notes.db")

SORT_OPTIONS = {
    "newest": "syntax_notes.id DESC",
    "oldest": "syntax_notes.id ASC",
    "syntax": "syntax_notes.syntax ASC",
}


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    # Step 1: Add a second table for categories and connect both tables.
    # This is a simple introduction to relational data and foreign keys.
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS syntax_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            syntax TEXT NOT NULL,
            explanation TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
        """
    )

    category_count = conn.execute("SELECT COUNT(*) FROM categories").fetchone()[0]

    if category_count == 0:
        categories = [
            ("Output",),
            ("Loops",),
            ("Conditions",),
        ]
        conn.executemany("INSERT INTO categories (name) VALUES (?)", categories)

    note_count = conn.execute("SELECT COUNT(*) FROM syntax_notes").fetchone()[0]

    if note_count == 0:
        examples = [
            ("print('Hello')", "Prints text to the console.", 1),
            ("for number in range(3):", "Repeats a block of code 3 times.", 2),
            ("if x > 10:", "Runs code only if the condition is true.", 3),
        ]
        conn.executemany(
            """
            INSERT INTO syntax_notes (syntax, explanation, category_id)
            VALUES (?, ?, ?)
            """,
            examples,
        )

    conn.commit()
    conn.close()


def get_all_categories():
    conn = get_db_connection()
    categories = conn.execute("SELECT id, name FROM categories ORDER BY name ASC").fetchall()
    conn.close()
    return categories


def category_exists(category_id):
    conn = get_db_connection()
    category = conn.execute(
        "SELECT id FROM categories WHERE id = ?",
        (category_id,),
    ).fetchone()
    conn.close()
    return category is not None


# Step 2: Use JOIN to read note data together with the category name.
# This keeps the templates simple because they receive all needed values directly.
def get_notes(search_query="", sort_query="newest"):
    conn = get_db_connection()
    order_by = SORT_OPTIONS.get(sort_query, SORT_OPTIONS["newest"])
    params = []
    sql = """
        SELECT
            syntax_notes.id,
            syntax_notes.syntax,
            syntax_notes.explanation,
            syntax_notes.category_id,
            categories.name AS category_name
        FROM syntax_notes
        JOIN categories ON categories.id = syntax_notes.category_id
    """

    if search_query:
        sql += """
        WHERE
            syntax_notes.syntax LIKE ?
            OR syntax_notes.explanation LIKE ?
            OR categories.name LIKE ?
        """
        pattern = f"%{search_query}%"
        params.extend([pattern, pattern, pattern])

    sql += f" ORDER BY {order_by}"
    notes = conn.execute(sql, params).fetchall()
    conn.close()
    return notes


def get_note_by_id(note_id):
    conn = get_db_connection()
    note = conn.execute(
        """
        SELECT
            syntax_notes.id,
            syntax_notes.syntax,
            syntax_notes.explanation,
            syntax_notes.category_id,
            categories.name AS category_name
        FROM syntax_notes
        JOIN categories ON categories.id = syntax_notes.category_id
        WHERE syntax_notes.id = ?
        """,
        (note_id,),
    ).fetchone()
    conn.close()
    return note


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
        categories=get_all_categories(),
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


# Step 3: Save the selected category id together with the note.
# The form now sends one extra value that belongs to the database model.
@app.post("/notes/create")
def create_note():
    syntax = request.form["syntax"].strip()
    explanation = request.form["explanation"].strip()
    category_id = request.form.get("category_id", "").strip()

    if not syntax or not explanation or not category_id:
        return (
            render_index_page(
                error_message="Syntax, explanation, and category are required.",
                form_data={
                    "syntax": syntax,
                    "explanation": explanation,
                    "category_id": category_id,
                },
            ),
            400,
        )

    if not category_exists(category_id):
        return (
            render_index_page(
                error_message="Please select a valid category.",
                form_data={
                    "syntax": syntax,
                    "explanation": explanation,
                    "category_id": category_id,
                },
            ),
            400,
        )

    conn = get_db_connection()
    conn.execute(
        """
        INSERT INTO syntax_notes (syntax, explanation, category_id)
        VALUES (?, ?, ?)
        """,
        (syntax, explanation, category_id),
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
    category_id = request.form.get("category_id", "").strip()
    note_to_edit = get_note_by_id(note_id)

    if note_to_edit is None:
        return redirect(url_for("index"))

    if not syntax or not explanation or not category_id:
        return (
            render_index_page(
                note_to_edit=note_to_edit,
                error_message="Syntax, explanation, and category are required.",
                form_data={
                    "syntax": syntax,
                    "explanation": explanation,
                    "category_id": category_id,
                },
            ),
            400,
        )

    if not category_exists(category_id):
        return (
            render_index_page(
                note_to_edit=note_to_edit,
                error_message="Please select a valid category.",
                form_data={
                    "syntax": syntax,
                    "explanation": explanation,
                    "category_id": category_id,
                },
            ),
            400,
        )

    conn = get_db_connection()
    conn.execute(
        """
        UPDATE syntax_notes
        SET syntax = ?, explanation = ?, category_id = ?
        WHERE id = ?
        """,
        (syntax, explanation, category_id, note_id),
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
