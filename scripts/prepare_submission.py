"""Create the lightweight-path evidence files required by the Lab 18 rubric.

Run after the notebooks have generated `_lakehouse/`:
    .venv/bin/python scripts/prepare_submission.py
or:
    make prepare-submission
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAKEHOUSE = ROOT / "_lakehouse"
OUT = ROOT / "submission" / "screenshots"
DELTA_LOG = LAKEHOUSE / "scratch" / "users_delta" / "_delta_log" / "00000000000000000000.json"


def main() -> int:
    if not LAKEHOUSE.exists():
        print("ERROR: _lakehouse/ not found. Run `make data`, `make data-ai`, and `make run-all` first.")
        return 1
    if not DELTA_LOG.exists():
        print(f"ERROR: expected Delta commit log not found: {DELTA_LOG}")
        print("Run NB1 / `make run-all` first.")
        return 1

    OUT.mkdir(parents=True, exist_ok=True)

    tree_file = OUT / "lakehouse_tree.txt"
    files = sorted(p.relative_to(ROOT).as_posix() for p in LAKEHOUSE.rglob("*") if p.is_file())
    tree_file.write_text("\n".join(files) + "\n", encoding="utf-8")

    log_file = OUT / "delta_log_sample.json"
    log_file.write_text(DELTA_LOG.read_text(encoding="utf-8"), encoding="utf-8")

    print(f"Wrote {tree_file.relative_to(ROOT)} ({len(files)} file paths)")
    print(f"Wrote {log_file.relative_to(ROOT)}")
    print("Submission evidence is ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
