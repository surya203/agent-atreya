# Atreya

A CrewAI crew that turns a coding task into a small full-stack project. Four specialists always run, in this order:

1. Tech lead writes the spec.
2. Backend engineer implements the FastAPI API.
3. Frontend engineer builds one HTML/JS page against that API.
4. QA engineer adds pytest coverage and a QA report.

CrewAI's hierarchical process can skip agents. This crew uses a sequential process so every specialist runs on every task. Each later task receives the earlier outputs as context.

## Setup

```text
uv sync
copy .env.example .env
```

Edit `.env` and set `OPENAI_API_KEY`. `MODEL` defaults to `gpt-4o-mini`. The crew calls the model and will not finish without a key.

## Run

```text
uv run python -m atreya.main examples/todo_task.txt
```

You can also pass the task as text:

```text
uv run python -m atreya.main "Add a health check endpoint and a page that shows its status"
```

Each run writes to `output/<timestamp>/`:

- `SPEC.md` from the tech lead
- `backend/` FastAPI app (`main.py`, `models.py`, `requirements.txt`)
- `frontend/` one page (`index.html`, `styles.css`, `app.js`)
- `tests/test_api.py` and `QA_REPORT.md` from QA

File tools can only read and write inside that run folder, and only these extensions: `.py`, `.html`, `.css`, `.js`, `.json`, `.md`, `.txt`.
