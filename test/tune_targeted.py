#!/usr/bin/env python3
"""Targeted EasyOCR conf tuner for MGS4, MGS5, and PeaceWalker using combined test sets."""
import os
import sys
import numpy as np
import easyocr
from PIL import Image, ImageEnhance

sys.path.insert(0, 'test')
sys.path.insert(0, 'test/new')
from ground_truth import GROUND_TRUTH
from ground_truth_new import GROUND_TRUTH_NEW

EXCLUDE = {'NRM'}

# Combined test data per game (old + new images)
GAME_FILES = {
    "mgs4": {
        "old": [("test", f) for f in ["near.webp", "mgs4_1.jpg", "mgs4_2.jpg", "mgs4_3.jpg", "mgs4_4.jpg", "mgs4_5.jpg"]],
        "new": [("test/new", f) for f in [f"mgs4_new_{i}.jpg" for i in range(1, 11)]],
        "contrast": 2.5, "subtitle_only": True,
    },
    "mgs5": {
        "old": [("test", f) for f in ["mgs5_1.jpg", "mgs5_2.jpg", "mgs5_3.jpg", "mgs5_4.jpg", "mgs5_5.jpg"]],
        "new": [("test/new", f) for f in [f"mgs5_new_{i}.jpg" for i in range(1, 11)]],
        "contrast": 2.0, "subtitle_only": True,
    },
    "peacewalker": {
        "old": [("test", f) for f in ["peacewalker_1.jpg", "peacewalker_2.jpg", "peacewalker_3.jpg", "peacewalker_4.jpg", "peacewalker_5.jpg"]],
        "new": [("test/new", f) for f in [f"peacewalker_new_{i}.jpg" for i in range(1, 11)]],
        "contrast": 2.5, "subtitle_only": False,
    },
}

CONF_VALUES = [0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8]


def preprocess(img, contrast, subtitle_only):
    if subtitle_only:
        w, h = img.size
        img = img.crop((0, int(h * 0.5), w, h))
    img = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)
    img = img.convert("L")
    img = ImageEnhance.Contrast(img).enhance(contrast)
    return img


def word_overlap(a, b):
    a_words = set(a.lower().split())
    b_words = set(b.lower().split())
    if not a_words and not b_words:
        return 1.0
    if not a_words or not b_words:
        return 0.0
    return len(a_words & b_words) / len(a_words | b_words)


def score_game(game, conf, reader, contrast, subtitle_only, all_files):
    correct, total = 0, 0
    for dirpath, filename in all_files:
        gt = GROUND_TRUTH_NEW.get(filename) or GROUND_TRUTH.get(filename)
        if not gt:
            continue
        path = os.path.join(dirpath, filename)
        if not os.path.exists(path):
            continue
        total += 1
        img = Image.open(path)

        # Codec detection (full image, low conf=0.3)
        full_img = preprocess(img, contrast, subtitle_only=False)
        full_arr = np.array(full_img)
        full_results = reader.readtext(full_arr)
        full_words = [t for _, t, c in full_results if c >= 0.3 and t.strip() and t.upper() not in EXCLUDE]
        full_text = ' '.join(full_words)
        is_codec = 'PTT' in full_text.upper() and 'TUNE' in full_text.upper()

        # Subtitle OCR at tested conf
        sub_img = preprocess(img, contrast, subtitle_only)
        sub_arr = np.array(sub_img)
        sub_results = reader.readtext(sub_arr)
        sub_words = [t for _, t, c in sub_results if c >= conf and t.strip() and t.upper() not in EXCLUDE]
        sub_text = ' '.join(sub_words)

        expected_type = gt['type']
        expected_text = gt['text']

        if is_codec:
            result, result_text = "CODEC", None
        elif len(sub_text) > 3:
            result, result_text = "TEXT", " ".join(sub_text.split())
        else:
            result, result_text = "NONE", None

        ok = False
        if expected_type == 'none':
            ok = result == "NONE"
        elif expected_type == 'codec':
            ok = result == "CODEC"
        elif expected_type in ('codec+dialogue', 'dialogue'):
            if result == "TEXT" and expected_text and result_text:
                ok = word_overlap(expected_text, result_text) > 0.4
            elif result == "CODEC" and expected_type == 'codec+dialogue':
                ok = True

        if ok:
            correct += 1

    return correct, total


if __name__ == '__main__':
    print("Loading EasyOCR model...")
    reader = easyocr.Reader(['en'], verbose=False)
    print("Ready.\n")

    for game, cfg in GAME_FILES.items():
        all_files = cfg['old'] + cfg['new']
        contrast = cfg['contrast']
        subtitle_only = cfg['subtitle_only']

        print(f"\n{'='*60}")
        print(f"{game} (contrast={contrast}, subtitle_only={subtitle_only})")
        print(f"{'='*60}")
        print(f"  {'conf':>6}  {'correct':>7}  {'total':>5}  {'pct':>5}")

        best_conf, best_score = 0.3, -1
        for conf in CONF_VALUES:
            correct, total = score_game(game, conf, reader, contrast, subtitle_only, all_files)
            pct = correct / total * 100 if total else 0
            marker = " <--" if pct > best_score else ""
            if pct > best_score:
                best_score = pct
                best_conf = conf
            print(f"  {conf:>6.2f}  {correct:>7}  {total:>5}  {pct:>4.0f}%{marker}")

        print(f"  => Best: conf={best_conf} ({best_score:.0f}%)")
