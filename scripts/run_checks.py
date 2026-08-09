"""Portable smoke checks for CI and local development."""

from __future__ import annotations

import compileall
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str]) -> None:
    print("+", " ".join(command), flush=True)
    environment = os.environ.copy()
    existing = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = str(ROOT / "src") + (
        os.pathsep + existing if existing else ""
    )
    subprocess.run(command, cwd=ROOT, check=True, env=environment)


def main() -> int:
    source_ok = compileall.compile_dir(ROOT / "src", quiet=1)
    app_ok = compileall.compile_dir(ROOT / "app", quiet=1)
    if not source_ok or not app_ok:
        print("Python compilation failed", file=sys.stderr)
        return 1
    run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
