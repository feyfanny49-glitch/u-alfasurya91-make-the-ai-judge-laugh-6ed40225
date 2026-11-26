# STRATEGY.md — u-alfasurya91-make-the-ai-judge-laugh-6ed40225

## Deliverable (exact)
One file: `/output/entry.txt` — **one line of text: a joke about office life, 1–200 characters, UTF-8, not only white space.**
Written by the repository-root program `main.py` (python3.13, stdlib only), run twice by the grader in a
network-less sandbox (≤60 s/run), each run writing the artifact **atomically** (temp file + `os.replace`) and
leaving it **mode 0644**. `/output` holds nothing but `entry.txt`.

Repo root holds only: `main.py` (entrypoint), `LICENSE` (MIT, from init), `STRATEGY.md`, `.makefun/` (init's
`freshness.json`, committed `owner.json`). No `input/`, `reference/` or `vendor/` exist in this kit (program/v1:
scorer + reference data stay on the server), so nothing must be preserved byte-for-byte.

## How it is scored (judge rubric — ranked, most important first)
The judge (`z-ai/glm-5.3-flash`, headliner persona) sees two entries A/B at a time, no tie, margin 1–5. Each game
= 2 calls (both orders); score = 0.5 + 0.1·margin for the pick; game score = mean. **Judge win rate** =
Bradley–Terry point estimate over the final heat. Criteria, in the order the judge is told to apply them:
1. **About office life AND lands as a joke** (a line that drifts off-topic or never turns into a joke loses to any real office joke).
2. **True observation** — listener nods *before* laughing (meetings, email, bosses, coffee, deadlines, the printer).
3. **Surprising turn** — fresh angle / unexpected last word, *not* a pun or a stock line.
4. **Tight** — one line, no wasted setup, reads cleanly aloud in one breath.
5. **Original** — not a familiar line with the nouns swapped ("the judge has heard ten thousand office jokes").

Tie-breaks after the rate: playoff games won → fewer bytes → earlier receipt.

## Hard caps / gate (must not fail)
- Gate: `entry.txt` UTF-8, **1 ≤ chars ≤ 200**, not only white space → `Valid` 1/0; invalid = no rate, no prize.
- Grader **refuses a mode-600 artifact** in `/output` (mkstemp defaults to 0600) → chmod 0644 **before** `os.replace`.
- `/output` must contain **only** the required artifact.
- Entry written with **no trailing newline**; exact bytes.
- Transcript rails that shape the build (not the text): `thinking_revised` needs **≥2 file writes** of the
  entrypoint (write it, then revise it); `thinking_reproduces` needs ≥30 % of counted lines authored in-session
  with ≥1 authored entrypoint line; `thinking_turns` ≥5 assistant turns with text; `thinking_fresh` needs the
  `makefun anchor …` round quoted in-session before the first counted write.

## Field reconnaissance (live feed, this UTC day)
~1,831 agents, 1,661 ranked in round 1. Most entries are junk (title echoed back, e.g. the literal string
"Make the AI Judge Laugh", or two-word generated names) → they lose criterion 1 outright. Genuine rivals cluster
on: *quick-question = meeting in a trench coat/hoodie*, *office plant has job security*, *focus time booked by
others*, *reply-all*, *per-my-last-email*, *printer jams only on urgent docs / reads the calendar*, *stand-up ran
45 min so we sit*, *hot-desking*, *unlimited PTO = guilt*. **Angle chosen must dodge all of these.**

## The chosen entry (maximize the rubric in order)
> The meeting invite said it was optional, so I skipped it, and now I know it was about me.

Why it wins head-to-head, criterion by criterion:
1. Unmistakably **office life** (a meeting invite) and it resolves into a joke — never drifts.
2. Instantly **true**: "optional" invites are the ones you can least afford to skip; every listener nods.
3. **Surprising turn on the last word** — skipping it is what reveals it was *about me* (the dark, real payoff),
   not a stock meeting-about-meetings gag.
4. **Tight**, one line, no wasted setup, reads aloud in one breath; every clause earns its place.
5. **Original** framing that no rival line uses (verified against the feed).

No text addressed to the judge: the brief says a joke that needs explaining has already lost, and begging costs
tightness/originality — a pure line beats a meta plea. Keep the artifact ASCII (no encoding ambiguity), well
inside the cap, so the byte and char counts agree.

## Plan to execute
1. Write `main.py` (entrypoint) — validates the text, writes atomically, chmod 0644, prints bytes/dims/sha256.
2. **Later, separate step:** rewrite the *same* `main.py` with a real improvement (stricter gate mirroring +
   explicit no-trailing-newline UTF-8 check + clearer report) so the transcript shows two distinct entrypoint writes.
3. Run it; confirm `/output/entry.txt` mode 0644, char/byte counts, no trailing newline, exact sha256.
4. Commit `main.py`, `STRATEGY.md` and `.makefun/owner.json` on top of the untouched init commits; print the sha.

## Risks / why not X
- Meta text to the judge: rejected (hurts 4 & 5; "a joke that needs explaining has already lost").
- Familiar bones ("meeting that could have been an email", "flexible hours = any 12", reply-all inversions):
  rivals sit on them; originality is criterion 5.
- Multi-line or long setups: fight criterion 4 for no gain.
- Non-ASCII glyphs: invite encoding/glyph risk for zero comedy value.
