"""The Funniest Honest Appliance Error — entry writer (v1).

Writes the tournament-winning one-line error message to entry.txt.
Pure stdlib, no clock, no randomness, no network: byte-identical output
on every run.
"""

import os
import sys

ENTRY = (
    "Washing machine: I leaked. The floor is wet. "
    "The warranty expired yesterday. I waited."
)


def output_dir():
    """Resolve the output directory: $MAKEFUN_OUTPUT_DIR, else /output, else this script's dir."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return env_dir
    if os.path.isdir("/output"):
        return "/output"
    return os.path.dirname(os.path.abspath(__file__))


def main():
    # Gate self-check (mirrors the sealed scorer): UTF-8, 1-200 chars,
    # one line, not blank. Written with no trailing newline so the file
    # is exactly len(ENTRY) characters.
    text = ENTRY
    assert 1 <= len(text) <= 200, "entry must be 1-200 characters"
    assert "\n" not in text and "\r" not in text, "entry must be one line"
    assert text.strip(), "entry must not be blank"
    text.encode("utf-8")  # raises if not valid UTF-8

    out_dir = output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
