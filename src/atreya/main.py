"""Run the developer crew on a task string or a task file."""

import argparse
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from atreya.crew import DevCrew


def resolve_task(value: str) -> str:
    path = Path(value)
    if path.is_file():
        return path.read_text(encoding="utf-8").strip()
    return value.strip()


def main(argv: list[str] | None = None) -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="Run the Atreya developer crew on a coding task."
    )
    parser.add_argument(
        "task",
        help="Task text, or a path to a text file containing the task.",
    )
    args = parser.parse_args(argv)

    task = resolve_task(args.task)
    if not task:
        print("Task is empty.", file=sys.stderr)
        return 1

    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = Path("output") / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    result = DevCrew(run_dir).crew().kickoff(inputs={"task": task, "run_id": run_id})
    print(result)
    print(f"\nWrote project to {run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
