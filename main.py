#!/usr/bin/env python3
"""Entry point for u-alfasurya91-make-the-ai-judge-laugh-6ed40225 (program/v1, judged text).

Deliverable: /output/entry.txt holds ONE text -- a joke about office life, UTF-8,
1..200 characters, not only white space. That single text is what the sealed gate
scores and what the judge reads, so this program's whole job is to place those exact
bytes on disk, atomically, in the one mode the grader accepts.

Gate mirrored here (so a bad build fails loudly at build time, never at the grader):
  * the text is non-empty, <= 200 characters, and not only white space;
  * it encodes to UTF-8 and decodes back byte-identically (no lone surrogates);
  * the artifact carries no leading white space and no trailing newline.

Write path: a temp file in the output directory (0600 from mkstemp) is filled,
flushed and fsync'd, chmod 0644'd *before* os.replace, then the result is re-read
from disk and compared byte-for-byte. The grader refuses a mode-600 artifact, so
the chmod must happen before the rename.
"""

import hashlib
import os
import sys
import tempfile

# The entry: one line, under 200 characters, about office life.
ENTRY = "The meeting invite said it was optional, so I skipped it, and now I know it was about me."

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200


def validate(text):
    """Return the entry's UTF-8 bytes, or raise ValueError if it would fail the gate."""
    if not isinstance(text, str) or text == "":
        raise ValueError("entry text is empty")
    if len(text) > MAX_CHARS:
        raise ValueError("entry text is %d characters, over the %d cap" % (len(text), MAX_CHARS))
    if text.strip() == "":
        raise ValueError("entry text is only white space")
    if text != text.strip():
        raise ValueError("entry text has leading or trailing white space")
    if text.endswith("\n"):
        raise ValueError("entry text must not end in a newline")
    data = text.encode("utf-8")
    if data.decode("utf-8") != text:
        raise ValueError("entry text does not round-trip through UTF-8")
    return data


def write_entry(path, data):
    """Write `data` to `path` atomically; chmod 0644 the temp file before the rename."""
    directory = os.path.dirname(path) or "."
    os.makedirs(directory, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".entry-", dir=directory)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(tmp, 0o644)
        os.replace(tmp, path)
        tmp = None
    finally:
        if tmp is not None and os.path.exists(tmp):
            os.unlink(tmp)


def main():
    data = validate(ENTRY)
    write_entry(OUTPUT_PATH, data)

    # Read the artifact back the way the grader will and confirm it is exactly right.
    with open(OUTPUT_PATH, "rb") as handle:
        on_disk = handle.read()
    if on_disk != data:
        raise SystemExit("artifact read back differs from the entry bytes")

    mode = os.stat(OUTPUT_PATH).st_mode & 0o777
    if mode != 0o644:
        raise SystemExit("artifact mode is %s, expected 0644" % oct(mode))
    if len(on_disk) != len(ENTRY.encode("utf-8")):
        raise SystemExit("artifact byte count mismatch")

    print("entry      : %s" % ENTRY)
    print("artifact   : %s" % OUTPUT_PATH)
    print("chars      : %d (cap %d)" % (len(ENTRY), MAX_CHARS))
    print("bytes      : %d" % len(on_disk))
    print("mode       : %s" % oct(mode))
    print("trailing-nl: %s" % ("yes" if on_disk.endswith(b"\n") else "no"))
    print("sha256     : %s" % hashlib.sha256(on_disk).hexdigest())
    return 0


if __name__ == "__main__":
    sys.exit(main())
