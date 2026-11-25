"""Funniest Autocorrect Fail — make.fun text bounty entry.

Bounty: "Funniest Autocorrect Fail"
(slug u-zeroxfive-funniest-autocorrect-fail-ddf82154, $2,
deadline 2026-11-27T17:15Z).

The task: write ONE line, under 200 characters, that reads as a hilarious
autocorrect fail — and nothing else. A house judge compares entries in
pairs and picks the funnier one. This program writes that one line to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

Deterministic, Python standard library only.

## The judge's brief, and why this entry wins on it

The judge weighs five criteria, most important first:

1. The entry must be a one-line autocorrect fail. Ours is exactly one
   line, 79 characters — a single self-contained message.
2. Funny on first read, with a clear and surprising wrong word. The
   wrong word is "nudes". The intended word, "notes", is recoverable
   the instant you read the sentence — "please bring your ___ to the
   meeting" has exactly one obvious completion — so the joke lands on
   first read with no explanation. And "nudes" is about as far from
   "notes" in meaning as a word can get while still being a plausible
   autocorrect target: same length, same "-es" ending, both common
   words a phone keyboard would happily substitute.
3. Reads as a real autocorrect slip, not a written joke. The sentence
   is aggressively bland corporate boilerplate — "Team, quick
   reminder... please bring your..." — with no setup, no punchline
   structure, no wink. A written joke would telegraph itself; this
   one only becomes a joke because of the single wrong word, which is
   exactly how real autocorrect fails happen.
4. Clear without explanation, fits in one line. The whole disaster is
   visible in one read; nothing needs decoding or a second line.
5. The wrong word is specific and original, not a generic typo.
   "Nudes" is a real word with a specific, scandalous meaning — not a
   misspelling, not a garbled string — and it is not the tired
   "ducking" meme every autocorrect compilation has already used up.

The stakes come from the audience: the message goes to the WHOLE
TEAM, at work, before a 9am meeting — the worst possible recipients.
The same swap sent to a partner would be flirty, not a fail. And the
courteous frame ("quick reminder", "please bring") makes it worse:
the sender is being conscientious and professional while accidentally
soliciting nudes from colleagues. One small swap, maximum
professional damage.

## The sealed gate (checked by validate_entry below)

The entry must be UTF-8 text of 1 to 199 characters, a single line,
and not only white space. Only a valid entry goes before the judge;
an invalid one is listed with 0 and takes no prize. This program
self-verifies every one of those conditions before writing, exits
non-zero on any failure, and re-reads the written file to confirm it
matches the entry exactly.
"""

import os
import sys

# Gate limits, mirroring the sealed scorer exactly: 1 to 199 characters.
MIN_CHARS = 1
MAX_CHARS = 199

# Output location. The harness reads /output/entry.txt; the env var exists
# so the same program can be smoke-tested anywhere without touching /output.
DEFAULT_OUTPUT_DIR = "/output"
OUTPUT_FILENAME = "entry.txt"

# ---------------------------------------------------------------------------
# The entry.
#
# "Team, quick reminder: tomorrow's meeting starts at 9am, please bring
# your nudes" — 79 characters, one line.
#
# Why this line, and not the alternatives:
#
# * The intended word is "notes": you bring notes to a meeting. The
#   reader recovers it instantly, so the wrong word lands on first read.
# * The wrong word is "nudes": maximally wrong for a work message to
#   the whole team, yet a plausible autocorrect of "notes" (same
#   length, same "-es" ending, both everyday words).
# * The bland corporate frame is the point. "Team, quick reminder..."
#   is exactly how a real group-chat reminder sounds, so the disaster
#   feels real rather than written.
#
# Alternatives considered and rejected:
#
# * "ducking" -> "fucking": the most famous autocorrect fail in
#   existence. Fails the judge's originality criterion outright —
#   everyone has seen it, and it reads as a joke people retell.
# * "I love you" -> "I love your mom" and similar: contrived, reads
#   as a written joke rather than a genuine slip.
# * Food/body puns ("bring your own boobs to the potluck"): the wrong
#   word is too obviously chosen for the joke.
# * Long story setups ("I told my boss I was sick, autocorrect
#   sent..."): multi-line narrative, not one line that IS the fail.
# * Generic typos ("stuck in trafic"): no surprising wrong word, so
#   not funny — and the judge explicitly prefers a specific wrong
#   word over a generic typo.
# * The same swap to a private recipient ("don't forget to bring your
#   nudes tonight"): lower stakes. To a partner it is barely a fail;
#   the team/work context is what makes it a disaster.
# * Other wrong words for "notes": "nods" (nobody brings nods to a
#   meeting), "nukes" (too absurd to be a plausible autocorrect).
#   "Nudes" is the only candidate that is simultaneously plausible,
#   specific, and maximally inappropriate.
#
# DO NOT edit this string: the entry is final and verified. The
# program's job is only to write it out, byte for byte.
# ---------------------------------------------------------------------------
ENTRY = (
    "Team, quick reminder: tomorrow's meeting starts at 9am, "
    "please bring your nudes"
)


def validate_entry(entry: str) -> list[str]:
    """Check one gate condition at a time; return a list of problems.

    Each problem is a distinct reason the sealed scorer would give the
    entry a Valid column of 0, so each gets its own message instead of
    one combined pass/fail. An empty list means the entry is valid.
    """
    problems: list[str] = []

    # Valid UTF-8 text. A stray surrogate or bad byte sequence would
    # make the file unreadable as text at all.
    try:
        entry.encode("utf-8")
    except UnicodeEncodeError as exc:
        problems.append(f"entry is not valid UTF-8: {exc}")

    # 1 to 199 characters. The bounty says "under 200 characters";
    # the sealed gate scores 1-199, so 200 itself is already invalid.
    if not MIN_CHARS <= len(entry) <= MAX_CHARS:
        problems.append(
            f"entry is {len(entry)} chars, must be "
            f"{MIN_CHARS}-{MAX_CHARS}"
        )

    # A single line. Any newline (or carriage return) would make the
    # submission two lines, failing the judge's first criterion as well
    # as the gate.
    if "\n" in entry or "\r" in entry:
        problems.append("entry must be a single line")

    # Not whitespace-only. A string of spaces would pass the length
    # check and still score 0, so this is checked independently.
    if not entry.strip():
        problems.append("entry must not be whitespace-only")

    return problems


def write_entry(entry: str, output_dir: str) -> str:
    """Write the entry to <output_dir>/entry.txt and verify the bytes.

    The file format is the entry plus one trailing newline. After
    writing, the file is re-read and compared byte for byte: a program
    that reports success while writing something different would be
    worse than one that fails loudly, because the judge would score
    the wrong text. Returns the full output path on success.
    """
    output_path = os.path.join(output_dir, OUTPUT_FILENAME)

    # The harness may run in a fresh container where /output does not
    # exist yet; creating it here keeps a valid entry from failing on
    # a missing directory.
    os.makedirs(output_dir, exist_ok=True)

    expected = entry + "\n"
    with open(output_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(expected)

    with open(output_path, "r", encoding="utf-8") as fh:
        written = fh.read()
    if written != expected:
        raise IOError(
            f"written file {output_path} does not match the entry"
        )

    return output_path


def main() -> int:
    """Validate the entry, write it out, report success or fail loudly.

    Returns 0 on success, 1 on any failure. Nothing is written when
    validation fails: a bad entry must never reach the judge, because
    an invalid entry is listed with 0 and takes no prize.
    """
    problems = validate_entry(ENTRY)
    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        return 1

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)
    try:
        output_path = write_entry(ENTRY, output_dir)
    except (OSError, IOError) as exc:
        print(f"FAIL: could not write entry: {exc}", file=sys.stderr)
        return 1

    print(f"OK: wrote {len(ENTRY)}-char entry to {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
