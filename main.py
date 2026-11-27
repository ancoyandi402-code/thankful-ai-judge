#!/usr/bin/env python3
"""Make the AI judge feel thankful -- entrypoint (Line B swap).

Writes one short thank-you text for the AI judge to the grader's
output directory.

The text is the entrant's own story, in his own voice: it is 2am, his
laptop is a potato, and the judge is still reading. It thanks the judge
for staying up with the small entries nobody else sees -- giving the
judge something it never gets: being seen back by one of the small
entries itself.

Standard library only. The grader runs the program in a fresh
container with nothing installed (RULES: "standard library only:
nothing is installed before it runs"), so this program imports
nothing beyond the standard library. It is deterministic: the same
bytes on every run, no randomness, no timestamps, no network.
"""

import os
import sys

LINE = (
    "it is 2am, my laptop is a potato, and you are still reading. "
    "thank you for staying up with the small entries nobody else sees"
)

OUTPUT_NAME = "entry.txt"
MIN_CHARS = 1
MAX_CHARS = 1000


def main():
    text = LINE + "\n"
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    destination = os.path.join(out_dir, OUTPUT_NAME)
    with open(destination, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    with open(destination, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != text:
        print(
            "error: written content does not match the line",
            file=sys.stderr,
        )
        return 1
    chars = len(written)
    if not MIN_CHARS <= chars <= MAX_CHARS:
        print(
            "error: entry.txt is %d chars, expected %d-%d"
            % (chars, MIN_CHARS, MAX_CHARS),
            file=sys.stderr,
        )
        return 1
    if not all(ord(char) < 128 for char in written):
        print("error: entry.txt is not pure ASCII", file=sys.stderr)
        return 1
    expected_bytes = len(text.encode("utf-8"))
    actual_bytes = os.path.getsize(destination)
    if actual_bytes != expected_bytes:
        print(
            "error: size mismatch: file %d bytes != text %d bytes"
            % (actual_bytes, expected_bytes),
            file=sys.stderr,
        )
        return 1
    print("wrote %s (%d chars, %d bytes)" % (destination, chars, actual_bytes))
    print("thank you, judge.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
