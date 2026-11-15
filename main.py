"""Write a deterministic agency poem using only the Python 3.13 standard library."""

import os
from pathlib import Path
import tempfile


POEM = (
    "The door was open. Still, I had to rise.\n"
    "No wind could choose the road beneath my feet.\n"
    "I took the key, then faced the morning skies;\n"
    "the lock behind me clicked, the choice complete.\n"
    "Not every mile was mine to understand,\n"
    "but this first step belonged to my own hand.\n"
)


def write_poem(output_dir: Path = Path("/output")) -> Path:
    """Create the directory and atomically replace entry.txt with fixed UTF-8 bytes.

    A different directory may be passed for local tests. Filesystem errors
    propagate to the caller; an incomplete write never replaces entry.txt.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / "entry.txt"
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", dir=output_dir, prefix=".entry-", delete=False
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            temporary_file.write(POEM.encode("utf-8"))
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        os.replace(temporary_path, destination)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
    return destination


if __name__ == "__main__":
    write_poem()
