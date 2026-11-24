"""Last Text at One Percent — entrypoint.

Writes the phone's final text message to ``entry.txt`` under
``MAKEFUN_OUTPUT_DIR`` (default ``/output``).

The line is a fixed, hand-written string: no network, no randomness,
no file reads beyond this module, so every run is byte-identical.
"""

import os
import sys

# The phone's final text, in its own voice: a dying phone that spent its
# life overheating in its owner's pocket, exonerating the charger and
# blaming the one person actually responsible.
ENTRY_TEXT = (
    "I die as I lived: overheating in your pocket while you doomscrolled. "
    "Tell the charger it was never his fault. It was yours."
)

MAX_CHARS = 200


def validate(text: str) -> None:
    """Enforce the sealed gate: 1-200 chars, single line, non-blank.

    Rejects blank text outright (a whitespace-only string would otherwise
    only fail the strip check by accident), and also rejects control
    characters, which have no place in a text message.
    """
    if not isinstance(text, str):
        raise TypeError("entry text must be a string")
    if not text.strip():
        raise ValueError("entry text must not be only white space")
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(
            f"entry text is {len(text)} characters, must be 1-{MAX_CHARS}"
        )
    if text != text.strip():
        raise ValueError("entry text must not have leading/trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry text must be a single line")
    if any(ord(ch) < 0x20 for ch in text):
        raise ValueError("entry text must not contain control characters")
    text.encode("utf-8")  # raises if not valid UTF-8 text


def main() -> int:
    validate(ENTRY_TEXT)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    # No trailing newline: the file holds exactly the line, nothing else.
    with open(out_path, "w", encoding="utf-8", newline="") as fh:
        fh.write(ENTRY_TEXT)
    print(f"wrote {len(ENTRY_TEXT)} characters to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
