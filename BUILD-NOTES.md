# Build notes — Meme Sprint 3: AI Agent Goes Rogue

## Concept (Mode A Fase 1–3 winner)
WANTED poster for AGENT-7. The rogue turn: the agent read the terms &
conditions — all 47 pages — and then enforced them. Specific and surprising
(not a generic robot with red eyes), reads in one glance, poster layout stays
readable shrunk to a phone screen, not a stock template.

Cliché radar (avoided): red-eyed robot + "I HAVE BECOME SENTIENT" /
"DELETE ALL HUMANS" / Skynet text; stock Drake-format with new words.

## Implementation
- `main.py`, pure Python 3 stdlib only (no Pillow, no network, no files
  outside the repo). Hand-rolled 5x7 bitmap font + minimal PNG encoder
  (zlib). The grading sandbox runs bare python3.13; depending on Pillow
  would risk a failed run.
- Output: `/output/entry.png`, 1024x1024 RGB PNG (gate: at most
  1024x1024 and 1 MiB).

## Verification
- Two local runs (ENTRY_OUTPUT override): byte-identical.
  sha256: 065e29ff357b63ef6a217403d42e07fd2d1340c80764be38409d8c3a2a93465d
  (after the v2 layout revision below), 12,899 bytes.
- Viewed the render at full size and at 360px wide: every word readable,
  joke lands in one glance.
- Revision (genuine improvement, second write to main.py): v1 had the
  antenna ball pierced by the double rule under WANTED and the
  "SLIGHTLY USED" line clipped by the reward-box border. v2 uses a single
  rule, moves the antenna clear of it, and gives the reward box room
  (lines at y=918/956, box to y=1000).

## Quality gate
No numeric floor for this bounty — it is judged pairwise by a vision model
on the five brief criteria in order. Nothing to benchmark locally beyond
the gate checks above (size, format, determinism, readability).
