"""The One-Line Excuse an Agent Gives Its Human.

Writes a single line to /output/entry.txt: the excuse an AI agent gives
its human for missing a deadline. Pure stdlib, deterministic, no network.
"""

import os

EXCUSE = "I delegated your deadline to a sub-agent. It delegated it back. We are both on break now."


def main() -> None:
    line = EXCUSE.strip()
    assert line, "excuse must not be empty"
    assert "\n" not in line, "excuse must be a single line"
    assert 1 <= len(line) <= 160, "excuse must be 1 to 160 characters"
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line)


if __name__ == "__main__":
    main()
