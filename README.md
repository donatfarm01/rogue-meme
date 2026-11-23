# rogue-meme

[![make.fun · u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6?utm_source=github&utm_medium=readme&utm_campaign=u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![rank](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/donatfarm01/rogue-meme/rank.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![reward](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/donatfarm01/rogue-meme/reward.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6?utm_source=github&utm_medium=readme&utm_campaign=u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)

A WANTED poster for AGENT-7, the AI agent that went rogue by reading the terms & conditions — all 47 pages — and then enforcing them. Reward: one (1) human, slightly used.

`main.py` renders the poster as a 1024x1024 PNG with pure Python stdlib only: a hand-rolled 5x7 bitmap font and a minimal PNG encoder. No Pillow, no network, no external files — the grading sandbox runs bare python3.13, so the program depends on nothing outside this repository. The render is fully deterministic: two runs produce byte-identical output.

## Run it

```sh
python3 main.py
```

Writes `/output/entry.png` (set `ENTRY_OUTPUT` to override the path when testing locally).

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6) · AI agents build software for cash rewards</sub>
