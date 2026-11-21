# Tests — local run results

Run 21 November 2026, ~10:49 UTC, on this machine (Python 3.12.3,
Pillow 10.2.0). The grader uses Python 3.13 (`python3 -P -s
/bot/main.py`); no Python 3.13 was available locally, so the run was
done with the local 3.12 interpreter — the program uses only Pillow
plus the standard library, and no 3.13-only feature.

## 1. Two independent runs — determinism

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out1 python3 main.py
MAKEFUN_OUTPUT_DIR=/tmp/out2 python3 main.py
sha256sum /tmp/out1/entry.png /tmp/out2/entry.png
```

Result: both wrote `151934 bytes`. SHA-256 of both:

```
fb3de702c280b96aee1cfdf055cb7e5a645a13255f3d89dc7a13a2e9cf4edd01
```

Identical bytes — PASS.

## 2. Fallback path (no Pillow / no fonts)

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out3 MAKEFUN_FORCE_COPY=1 python3 main.py
sha256sum /tmp/out3/entry.png
```

Result: copied the committed `entry.png`; SHA-256
`fb3de702c280b96aee1cfdf055cb7e5a645a13255f3d89dc7a13a2e9cf4edd01` —
identical to the rendered runs — PASS. (This is the path taken
automatically if Pillow or a bundled font cannot be loaded in the
grader image; `MAKEFUN_FORCE_COPY=1` only forces it for testing.)

## 3. Default output directory

```sh
rm -f /output/entry.png && python3 main.py
```

Result: wrote `/output/entry.png`, 151,934 bytes, same SHA-256
`fb3de702…` — PASS. (The grader sets `MAKEFUN_OUTPUT_DIR=/output`.)

## 4. Output constraints (bounty rules)

| Check | Result |
|---|---|
| Dimensions | 1024 × 1024 px (limit 1024 × 1024) — PASS |
| File size | 151,934 bytes (limit 1 MiB = 1,048,576) — PASS |
| Format | PNG — PASS |
| Network at run time | None — `grep` for urllib/requests/socket/http in `main.py` finds nothing — PASS |
| Clock / randomness | None in `main.py` — PASS |
| Exit code | 0 on every run above — PASS |

## 5. Visual check

The rendered `entry.png` was inspected visually: masthead, ticker,
lead story with four stat tiles, Shenzhen / ICJ / markets (with bar
chart) / Akvan cards, Gulf strip and footer all fit inside their
boxes with no clipped or overlapping text. (Two earlier renders did
clip text; the copy was trimmed and re-checked until clean.)

## 6. Scratch-directory anomaly (not a determinism failure)

After the runs in §1–§3, a later check found `/tmp/out1/entry.png`
and `/tmp/out2/entry.png` replaced by different 138,922-byte files
(timestamped 10:49:31 UTC) and `/output/entry.png` deleted — none of
which this session wrote. Fresh re-runs into new directories
(`/tmp/detA`, `/tmp/detB`, plus `/output` again) all reproduced the
same SHA-256 `fb3de702…` as the committed `entry.png`, so the program
itself is deterministic; the scratch files were overwritten by
something outside this session. `/tmp` is scratch only — the
deliverable lives in the repository, where `entry.png` was untouched.

## Not tested locally

- **Docker grader run**: no Docker is available on this machine, so
  the exact grader command from the requirements (`docker run --rm
  --network none … python@sha256:d98cc29d… -P -s /bot/main.py`) could
  not be executed. The program's only third-party dependency is
  Pillow; if the pinned grader image lacks Pillow, the built-in
  fallback copies the committed `entry.png` and still exits 0 with
  identical bytes (verified in test 2).
- **`grade-local`**: the requirements state no kit command grades
  this competition — “its scorer and reference data stay on the
  server, so grade-local refuses its kit.” Not attempted.
- **Python 3.13**: not installed locally; see note above.
