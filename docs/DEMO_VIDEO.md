# DEMO VIDEO — 60-second reproducible walkthrough

> Best practice 2026 (RepoClip / RapidDev / screencli): GitHub strips `<iframe>`.
> Use YouTube-thumbnail link, native `user-attachments` MP4, or autoplay GIF. No hand-waved numbers —
> every on-screen figure is `results/run-*.json` seed 7.

## Storyboard (`assets/demo_walkthrough.html`)

| Time | Narration | Command on screen | Verified overlay |
|---|---|---|---|
| 0:00 | "Frozen SPEC v1.0, seed 7. Pipeline proof first." | `python3 src/exp00_synthetic.py` | loc/absorp/fail2 True, n=1 |
| 0:15 | "Public 5-minute NQ, RTH only, 950 bars." | `python3 src/exp04_public_intraday.py` | 78 hits → 40 blocked → n=22 PF 2.39 |
| 0:30 | "Deflate against the field on the same bars." | `python3 src/exp05_benchmarks.py` | DSR 0.62 FAIL, RC 0.80, buy-hold 4.64 wins |
| 0:45 | "Purged walk-forward + Monte Carlo." | `python3 src/exp07_wfa_mc.py` | 3/4 PASS, t 1.81, CI includes 0, MC degenerate |
| 1:00 | "Paper trail. Tape + GEX remain TODO." | `python3 src/exp06_paper.py` | `docs/PAPER_RESULTS.md` |

## Record (OBS, 720p, <10 MB)

1. `python3 src/make_visuals.py` (rebuilds `assets/*.png`)
2. Open `assets/demo_walkthrough.html` in Chrome (Playwright-verified: `assets/demo_preview.png`)
3. OBS: record 60 s scrolling storyboard + terminal runs above
4. HandBrake: 720p, H.264, <10 MB → `assets/demo.mp4` (git-ignored until upload)

## Publish (pick one)

- **YouTube (recommended):** upload, get `VIDEO_ID`, paste thumbnail markdown from `README.md` Demo section.
- **Native:** drag-drop `assets/demo.mp4` into a GitHub issue comment → copy `user-attachments/assets/...` URL → embed (inline player, no YouTube).
- **GIF:** `npx screencli export ./recordings/demo --preset github-gif` → `assets/demo.gif` (<8 MB, autoplay).

## Verify before push

- [ ] Every number on screen matches `results/run-*.json` (seed 7)
- [ ] `HYPOTHETICAL (CFTC 4.41)` caption visible throughout
- [ ] `docs/DISCLOSURE.md` linked below video
- [ ] Preview tab shows player/thumbnail/GIF correctly
