# Rate My Teacher

"Know the class before you take the class." Students anonymously rate teachers on
difficulty, workload, clarity, test difficulty, and participation, and see an
overall letter grade.

## How it's built

- **Backend:** Python + [Flask](https://flask.palletsprojects.com/) — see `app.py`
- **Database:** SQLite — a single file (`ratemyteacher.db`), created automatically the
  first time you run the app. No separate database server needed.
- **Frontend:** plain HTML (in `templates/`), CSS (`static/css/style.css`), and a
  little JS (`static/js/main.js`) — no frontend framework, no build step.

## Project structure
