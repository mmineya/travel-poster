"""Publish the atmospheric Port Lumen artwork; rendering is a local build step."""

import os
from pathlib import Path
import shutil

OUTPUT_FILENAME = "entry.png"


def publish(output_dir: Path) -> Path:
    """Copy the shipped PNG into the exact requested directory, creating parents."""
    output_dir.mkdir(parents=True, exist_ok=True)
    source = Path(__file__).resolve().with_name(OUTPUT_FILENAME)
    target = output_dir / OUTPUT_FILENAME
    if source.resolve() != target.resolve():
        shutil.copyfile(source, target)
    return target


def main() -> None:
    publish(Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")))


if __name__ == "__main__":
    main()
