"""Read and write project files inside a single crew run directory."""

from pathlib import Path
from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

ALLOWED_SUFFIXES = {".py", ".html", ".css", ".js", ".json", ".md", ".txt"}


class SaveProjectFileInput(BaseModel):
    path: str = Field(..., description="Path relative to the run directory, such as backend/main.py.")
    content: str = Field(..., description="Full text contents to write.")


class ReadProjectFileInput(BaseModel):
    path: str = Field(..., description="Path relative to the run directory, such as backend/main.py.")


def resolve_inside(run_dir: str, relative: str) -> Path:
    """Return a path that stays inside run_dir and uses an allowed extension."""
    if not relative or not relative.strip():
        raise ValueError("path is required")

    raw = relative.strip().replace("\\", "/")
    if raw.startswith("/") or raw.startswith("//"):
        raise ValueError("absolute paths are not allowed")

    candidate = Path(raw)
    if candidate.is_absolute() or candidate.drive:
        raise ValueError("absolute paths are not allowed")
    if any(part == ".." for part in candidate.parts):
        raise ValueError("path traversal is not allowed")

    root = Path(run_dir).resolve()
    target = (root / candidate).resolve()
    if target != root and root not in target.parents:
        raise ValueError("path escapes the run directory")

    if target.suffix.lower() not in ALLOWED_SUFFIXES:
        allowed = ", ".join(sorted(ALLOWED_SUFFIXES))
        raise ValueError(f"extension {target.suffix or '(none)'} is not allowed; use one of {allowed}")

    return target


class SaveProjectFileTool(BaseTool):
    name: str = "save_project_file"
    description: str = (
        "Write a text file inside the current run directory. "
        "path is relative, for example backend/main.py or frontend/index.html. "
        "Allowed extensions: .py, .html, .css, .js, .json, .md, .txt."
    )
    args_schema: Type[BaseModel] = SaveProjectFileInput
    run_dir: str

    def _run(self, path: str, content: str) -> str:
        try:
            if content is None or not str(content).strip():
                return "Error: content is empty"
            target = resolve_inside(self.run_dir, path)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        except Exception as exc:
            return f"Error: {exc}"
        return f"Wrote {path}"


class ReadProjectFileTool(BaseTool):
    name: str = "read_project_file"
    description: str = (
        "Read a text file inside the current run directory. "
        "path is relative, for example backend/main.py or SPEC.md."
    )
    args_schema: Type[BaseModel] = ReadProjectFileInput
    run_dir: str

    def _run(self, path: str) -> str:
        try:
            target = resolve_inside(self.run_dir, path)
            if not target.is_file():
                return f"Error: file not found: {path}"
            return target.read_text(encoding="utf-8")
        except Exception as exc:
            return f"Error: {exc}"
