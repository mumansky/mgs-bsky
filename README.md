# Metal Gear Solid Bluesky Bot

[@randommetalgear.bsky.social](https://bsky.app/profile/randommetalgear.bsky.social) — posts random screenshots from Metal Gear Solid 1–5, Twin Snakes, and Peace Walker every 30–45 minutes, with OCR-generated alt text.

## How it works

1. Picks a random game and extracts a random frame from a local `.mp4` file
2. Runs per-game OCR to detect on-screen text (dialogue, codec subtitles)
3. Detects codec screens by scanning for the keywords PTT and TUNE
4. Generates alt text and posts to Bluesky via `atproto`

Two OCR engines are used, tuned independently per game:

| Game         | Engine     | Notes                        |
|--------------|------------|------------------------------|
| MGS1         | Tesseract  | Bottom 50% crop              |
| MGS2         | Tesseract  | Bottom 50% crop, high conf   |
| MGS3         | EasyOCR    | Full frame                   |
| MGS4         | EasyOCR    | Bottom 50% crop              |
| MGS5         | EasyOCR    | Bottom 50% crop              |
| Twin Snakes  | Tesseract  | Bottom 50% crop              |
| Peace Walker | EasyOCR    | Full frame (all-caps text)   |

## Running

```bash
# Bot
python main-bsky.py

# Test suite (111 labelled frames)
python test_suite.py

# Filter to one game
python test_suite.py mgs3
```

## Dependencies

```bash
pip install atproto opencv-python pytesseract easyocr pillow
```

Tesseract must also be installed at the system level (`brew install tesseract` / `apt install tesseract-ocr`).

## Required local files (gitignored)

- `mgs1.mp4` through `mgs5.mp4`, `twinsnakes.mp4`, `peacewalker.mp4`
- `credentialsbsky.py` — contains `app_password = "..."` for the Bluesky app password

## Deployment

Runs on a Raspberry Pi 5 via systemd. See `mgs-bot.service`.

## Test suite

111 ground-truth labelled frames across all 7 games (41 original + 70 extended, extracted with `random.seed(42)`). Ground truth lives in `test/ground_truth.py`. Tuning scripts are in `test/`.
