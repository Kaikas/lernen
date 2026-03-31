# AGENTS.md

## Project Purpose

This project is a small learning app for students who are training to become `Fachinformatiker`.
The app is meant to be easy to read, easy to extend, and useful for programming lessons.

## Main Goal

The app helps learners collect Python syntax examples and write down what each example does.
The repository should support this with complete lesson folders that learners can open one by one.

## Repository Structure

- `lesson_1_base_app` is the clean base project.
- `lesson_2_edit_notes` builds on the base project and adds the edit feature.
- `lesson_3_note_details` builds on lesson 2 and adds a detail page for one note.
- `lesson_4_search_notes` builds on lesson 3 and adds search.
- `lesson_5_sort_notes` builds on lesson 4 and adds safe sorting.
- `lesson_6_validation_messages` builds on lesson 5 and adds validation and error messages.
- `lesson_7_note_categories` builds on lesson 6 and adds a second table with categories and joins.
- `lesson_8_category_summary` builds on lesson 7 and adds SQL aggregation with `COUNT` and `GROUP BY`.
- Each lesson folder should remain a complete small project with its own `app.py`, `templates/`, `pyproject.toml`, and `README.md`.
- Prefer adding new learning steps as new lesson folders instead of mixing multiple lesson stages into one file.

## Audience

- Students in vocational training for `Fachinformatiker`
- Teachers, tutors, or mentors who use the project for programming lessons

## Development Rules

- Keep the code simple and beginner-friendly.
- Prefer clarity over clever or compact solutions.
- Use small functions and straightforward control flow.
- Avoid unnecessary abstractions, frameworks, or advanced patterns.
- Keep the database layer easy to understand.
- Add short comments only when they help learners understand the code.

## Language Rules

- Everything user-facing must be in English.
- Code identifiers should be in English.
- Route names should be in English.
- Database table names and column names should be in English.
- Documentation for this project should be in English unless there is a strong reason not to.

## Tech Expectations

- Use Flask for the web app.
- Use SQLite for persistence unless there is a clear teaching reason to change it.
- Use `uv` for dependency management and running the project.

## UI Expectations

- Keep the interface simple and readable.
- Prefer plain HTML forms and basic styling over complex frontend tooling.
- Make the app understandable for beginners who are just learning web development.

## Change Policy

- Changes should support teaching and learning first.
- New features should stay small and easy to explain.
- If a feature adds complexity, document why it is worth it for learners.
- Keep lesson folders clearly separated so learners can switch directories and compare full project states.
