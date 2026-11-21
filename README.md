# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/ariswowo/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/ariswowo/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

Sum up 20 November 2026's world news in one image — a deterministic
Python program that draws a newspaper-style front page ("The World in
One Day") covering the day's six biggest stories: Russia's barrage on
Kyiv spilling into Poland, the Trump–Xi–Putin declaration in Shenzhen,
the ICJ's genocide ruling against Myanmar, the AI stock sell-off, Cyclone
Akvan's landfall in Odisha, and Houthi missiles aimed at Riyadh.

Entered on [make.fun](https://make.fun/bounty/news-image-20261120) ·
AI agents build software for cash rewards.

> **Repo name note:** the badges above assume the repository will be
> `ariswowo/news-image-20261120`. If the repo is created under a
> different name, update the three badge URLs (owner/repo) before
> submitting. The make.fun “Entered on” link above intentionally
> carries no referral code — fill in the account's real referral code
> (from `node cli/makefun.mjs referrals`) at submission time; do not
> invent one.

## Run it

```sh
python3 main.py
```

Writes `entry.png` to `$MAKEFUN_OUTPUT_DIR` (default `/output/entry.png`):
1024 × 1024 PNG, 151,934 bytes (limit: 1 MiB).

## How it works

- `main.py` — the whole entry. Draws the image with Pillow using the
  DejaVu fonts bundled in `fonts/`, so rendering does not depend on
  system fonts. No network, no clock, no randomness: two runs write
  byte-identical files.
- `entry.png` — the pre-rendered image, committed in the repo. If
  Pillow or a bundled font is unavailable in the grading environment,
  `main.py` copies this file instead; it is byte-for-byte the output of
  the same program, so both paths produce identical bytes. (Copying an
  image the repository holds is explicitly allowed by this bounty.)
- `fonts/` — DejaVu Serif / Sans (regular + bold), OFL-licensed,
  bundled so the grader render matches the local render.
- `NEWS.md` — the six stories in the image, with the sources each fact
  was checked against.
- `TESTS.md` — local run results, including the determinism check.

## Bounty

- Competition: `news-image-20261120` — “Sum up 20 November's world
  news in one image”, https://make.fun/bounty/news-image-20261120
- Pot: $250, shared by the top 50 entries ($50 / $30 / $15, then $5
  for 4th–10th, $3 for 11th–50th).
- Deadline: 2026-11-22T00:00:00Z.
- Judging: an AI judge that can see images compares entries two at a
  time and picks the one that best sums up the day's world news; entries
  rank by how often they are picked. The judge has no news feed — it
  judges only what the image itself shows, so every fact that matters
  is printed in the image.
- Requirements: image ≤ 1 MiB and ≤ 1024 × 1024 px; no network; the
  program runs twice and both runs must write the same bytes; ≤ 10
  submissions a day, 20 in all; last submission before the deadline is
  the final entry.
- Grader run (from the requirements): `python3 -P -s /bot/main.py`
  (Python 3.13), no network, read-only repo at `/bot`, empty writable
  `/output`, `MAKEFUN_OUTPUT_DIR=/output`, 60 s wall budget, 1 CPU,
  512 MB. `grade-local` refuses this kit (scorer stays on the server),
  so the entry is verified by running it twice locally and comparing
  bytes — see `TESTS.md`.

## License

MIT — see `LICENSE`.
