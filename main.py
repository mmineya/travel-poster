"""Publish the pre-rendered Port Lumen poster using only the standard library."""

import os
from pathlib import Path
import shutil


def main() -> None:
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    source = Path(__file__).resolve().with_name("entry.png")
    target = output_dir / "entry.png"
    if source.resolve() != target.resolve():
        shutil.copyfile(source, target)


if __name__ == "__main__":
    main()
