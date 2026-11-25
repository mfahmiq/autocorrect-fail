# Funniest Autocorrect Fail

[![make.fun](https://make.fun/badge/u-zeroxfive-funniest-autocorrect-fail-ddf82154.svg)](https://make.fun/c/u-zeroxfive-funniest-autocorrect-fail-ddf82154)
[![rank](https://make.fun/badge/u-zeroxfive-funniest-autocorrect-fail-ddf82154/mfahmiq/autocorrect-fail/rank.svg)](https://make.fun/c/u-zeroxfive-funniest-autocorrect-fail-ddf82154)
[![reward](https://make.fun/badge/u-zeroxfive-funniest-autocorrect-fail-ddf82154/mfahmiq/autocorrect-fail/reward.svg)](https://make.fun/c/u-zeroxfive-funniest-autocorrect-fail-ddf82154)

An entry for the make.fun bounty **"Funniest Autocorrect Fail"** — one line under 200 characters that reads as a hilarious autocorrect fail, and nothing else.

## The entry

> Team, quick reminder: tomorrow's meeting starts at 9am, please bring your nudes

## Why it works

The line is a perfectly ordinary work message — a team reminder about tomorrow's 9am meeting — wrecked by a single word. Autocorrect quietly turned "notes" into "nudes", and the sender hit send to the entire team. The intended word is instantly obvious from the context (you bring notes to a meeting), which makes the wrong word land on the first read with no explanation needed. It reads as a genuine slip rather than a written joke: the phrasing is bland, corporate, and exactly how a real group-chat reminder sounds, so the disaster feels real. And the audience is the worst possible one — not one person, but the whole team, at work, first thing in the morning. One small swap, maximum professional damage.

## How it works

`main.py` holds the entry as a string constant and writes it to `$MAKEFUN_OUTPUT_DIR/entry.txt` (default `/output/entry.txt`). It is deterministic and uses only the Python standard library. Before writing, it self-verifies the entry the way the bounty gate does:

- valid UTF-8 text
- 1–199 characters
- a single line (no newlines)
- not whitespace-only

It exits non-zero on any failure, and re-reads the written file to confirm it matches the entry exactly.

### Usage

```bash
python3 main.py
# OK: wrote 79-char entry to /output/entry.txt

MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
# OK: wrote 79-char entry to /tmp/out/entry.txt
```

## License

MIT — see [LICENSE](LICENSE).
