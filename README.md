# Simple Flask App with SQLite

This repository now contains complete lesson folders.

## Install

Change into one lesson folder first, then run:

```bash
uv sync
```

## Structure

- `lesson_1_base_app`: complete base project with create, read, and delete
- `lesson_2_edit_notes`: complete project that adds editing step by step
- `lesson_3_note_details`: complete project that adds a detail page for one note
- `lesson_4_search_notes`: complete project that adds search with query strings
- `lesson_5_sort_notes`: complete project that adds sorting for the note list
- `lesson_6_validation_messages`: complete project that adds validation and error messages
- `lesson_7_note_categories`: complete project that adds a second table and SQL joins
- `lesson_8_category_summary`: complete project that adds SQL aggregation with `GROUP BY`

Each lesson folder contains its own `app.py`, `templates/`, `pyproject.toml`, and `README.md`.

## Learning path

1. Change into `lesson_1_base_app`
2. Read and run the base project
3. Change into `lesson_2_edit_notes`
4. Compare both folders and follow the numbered comments in lesson 2
5. Change into `lesson_3_note_details`
6. Add the next "read" feature: a page for one single note
7. Change into `lesson_4_search_notes`
8. Learn filtering with query strings and SQL `LIKE`
9. Change into `lesson_5_sort_notes`
10. Learn safe sorting with a whitelist for `ORDER BY`
11. Change into `lesson_6_validation_messages`
12. Learn form validation and error handling
13. Change into `lesson_7_note_categories`
14. Learn relational data with categories and `JOIN`
15. Change into `lesson_8_category_summary`
16. Learn SQL aggregation with `COUNT` and `GROUP BY`

## Learning note

The later lesson folders explain their new feature directly in the code with numbered comments.
This keeps the base project clean and each later lesson focused on one feature.

## Important files

- `lesson_1_base_app/app.py`: base app
- `lesson_1_base_app/templates/index.html`: base UI
- `lesson_2_edit_notes/app.py`: lesson 2 app
- `lesson_2_edit_notes/templates/index.html`: lesson 2 UI
- `lesson_3_note_details/app.py`: lesson 3 app
- `lesson_3_note_details/templates/index.html`: lesson 3 list page
- `lesson_3_note_details/templates/detail.html`: lesson 3 detail page
- `lesson_4_search_notes/app.py`: lesson 4 app
- `lesson_5_sort_notes/app.py`: lesson 5 app
- `lesson_6_validation_messages/app.py`: lesson 6 app
- `lesson_7_note_categories/app.py`: lesson 7 app
- `lesson_8_category_summary/app.py`: lesson 8 app
