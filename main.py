"""One-line excuse writer for the make.fun bounty.

The program assembles the entry line from its sentence fragments,
checks the result against the competition gate (one line, between 1
and 160 characters, valid UTF-8, nothing but the line itself), and
writes those exact bytes to the output path. It uses only the Python
standard library, reads nothing from the network, and always produces
the same file.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Where the graded entry goes when no path is given on the command line.
DEFAULT_OUTPUT = "/output/entry.txt"

# The upper bound the kit gate puts on an entry.
MAX_CHARACTERS = 160

# The entry, kept as its three sentences so the line is built rather
# than pasted. Joining with single spaces is what fixes the wording.
SENTENCES = (
    "I delegated your deadline to a sub-agent.",
    "It delegated it back.",
    "We are both on break now.",
)


def assemble_line() -> str:
    """Join the sentence fragments into the single entry line."""
    return " ".join(SENTENCES)


def gate_problems(line: str) -> list[str]:
    """Return every way the line would fail the kit gate, or nothing."""
    problems: list[str] = []
    if not line:
        problems.append("entry is empty")
    if line != line.strip():
        problems.append("entry has leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        problems.append("entry spans more than one line")
    if not 1 <= len(line) <= MAX_CHARACTERS:
        problems.append(
            f"entry is {len(line)} characters, gate allows 1 to "
            f"{MAX_CHARACTERS}"
        )
    try:
        line.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("entry is not valid UTF-8 text")
    return problems


def resolve_destination(argv: list[str]) -> Path:
    """Pick the output path: first argument, or the kit default."""
    if len(argv) > 2:
        raise SystemExit("usage: main.py [output-path]")
    return Path(argv[1]) if len(argv) == 2 else Path(DEFAULT_OUTPUT)


def emit(line: str, destination: Path) -> int:
    """Write the line as UTF-8 bytes, then confirm what landed on disk."""
    payload = line.encode("utf-8")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(payload)
    if destination.read_bytes() != payload:
        raise SystemExit(f"verification failed: {destination} differs")
    return len(line)


def main(argv: list[str]) -> int:
    """Assemble, gate-check, and write the entry line."""
    line = assemble_line()
    problems = gate_problems(line)
    if problems:
        for problem in problems:
            print(f"invalid entry: {problem}", file=sys.stderr)
        return 1
    destination = resolve_destination(argv)
    count = emit(line, destination)
    print(f"wrote {count} characters to {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
