"""The Excuse That Almost Works - the one line a gamer texts the boss to
get out of work during GTA 6 launch week.

The program writes the text to $MAKEFUN_OUTPUT_DIR/entry.txt (default
/output), with no trailing newline. The bounty's gate: entry.txt must be
UTF-8 text of 1 to 140 characters, not only whitespace, and the line must
be at most 20 words.
"""

import os

TEXT = "Water's off in my whole street till 2pm and I can't shower, I'm not coming in smelling like yesterday."
# Why this line: the judge is a tired manager who has heard every excuse
# twice, so the line wins by being boring, specific and honest instead of
# dramatic - a whole-street water outage is a real, checkable, mundane
# detail, not a dead grandmother, a flat tyre or a sudden fever. The laugh
# comes from the excuse's own logic: it admits the embarrassing truth
# (no shower) instead of inventing a tragedy, and "smelling like
# yesterday" is the kind of blunt line a real person texts in a hurry.
# It almost works because it is true-sounding and specific - and it almost
# doesn't, because a strict manager could still say "come in anyway".


def gate(text):
    """Check the gate: UTF-8, 1-140 chars, at most 20 words, not only
    whitespace, no leading or trailing whitespace, a single line."""
    if not isinstance(text, str):
        raise ValueError("entry is not text")
    text.encode("utf-8")
    if not 1 <= len(text) <= 140:
        raise ValueError("entry is %d chars, gate is 1-140" % len(text))
    if len(text.split()) > 20:
        raise ValueError("entry is %d words, limit is 20" % len(text.split()))
    if not text.strip():
        raise ValueError("entry is only whitespace")
    if text != text.strip():
        raise ValueError("entry has leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return True


def main():
    gate(TEXT)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(TEXT)
    os.chmod(path, 0o644)
    with open(path, "rb") as f:
        raw = f.read()
    read_back = raw.decode("utf-8")
    if read_back != TEXT:
        raise ValueError("read-back differs from TEXT")
    if len(raw) != len(TEXT.encode("utf-8")):
        raise ValueError("written bytes differ from TEXT bytes")
    gate(read_back)
    print("wrote %d chars to %s" % (len(TEXT), path))


if __name__ == "__main__":
    main()
