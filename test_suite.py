#!/usr/bin/env python3
"""OCR pipeline test suite — runs all 111 labelled frames across 7 games."""
import os
import sys
import numpy as np
import pytesseract
import easyocr
from PIL import Image, ImageEnhance

from test.ground_truth import GROUND_TRUTH

WHITELIST = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,!?' -"
EXCLUDE = {'NRM'}

OCR_CONFIG = {
    "mgs1":        {"engine": "tesseract", "contrast": 2.0, "psm": 6,  "conf": 60,  "subtitle_only": True},
    "mgs2":        {"engine": "tesseract", "contrast": 2.0, "psm": 11, "conf": 90,  "subtitle_only": True},
    "mgs3":        {"engine": "easyocr",   "contrast": 2.5, "conf": 0.6, "subtitle_only": False},
    "mgs4":        {"engine": "easyocr",   "contrast": 2.5, "conf": 0.75, "subtitle_only": True},
    "mgs5":        {"engine": "easyocr",   "contrast": 2.0, "conf": 0.8, "subtitle_only": True},
    "twinsnakes":  {"engine": "tesseract", "contrast": 2.0, "psm": 6,  "conf": 80,  "subtitle_only": True},
    "peacewalker": {"engine": "easyocr",   "contrast": 2.5, "conf": 0.55, "subtitle_only": False},
}

# All test images grouped by game, referenced by repo-relative path
GAME_MAP = {
    "mgs1": [
        "test/mgs1.jpg", "test/mgs1_1.jpg", "test/mgs1_2.jpg", "test/mgs1_3.jpg",
        "test/mgs1_4.jpg", "test/mgs1_5.jpg",
        *[f"test/new/mgs1_new_{i}.jpg" for i in range(1, 11)],
    ],
    "mgs2": [
        "test/mgs2.jpg", "test/codec.webp", "test/mgs2_1.jpg", "test/mgs2_2.jpg",
        "test/mgs2_3.jpg", "test/mgs2_4.jpg", "test/mgs2_5.jpg",
        *[f"test/new/mgs2_new_{i}.jpg" for i in range(1, 11)],
    ],
    "mgs3": [
        "test/mgs3.jpg", "test/mgs3_1.jpg", "test/mgs3_2.jpg", "test/mgs3_3.jpg",
        "test/mgs3_4.jpg", "test/mgs3_5.jpg",
        *[f"test/new/mgs3_new_{i}.jpg" for i in range(1, 11)],
    ],
    "mgs4": [
        "test/near.webp", "test/mgs4_1.jpg", "test/mgs4_2.jpg", "test/mgs4_3.jpg",
        "test/mgs4_4.jpg", "test/mgs4_5.jpg",
        *[f"test/new/mgs4_new_{i}.jpg" for i in range(1, 11)],
    ],
    "mgs5": [
        "test/mgs5_1.jpg", "test/mgs5_2.jpg", "test/mgs5_3.jpg", "test/mgs5_4.jpg",
        "test/mgs5_5.jpg",
        *[f"test/new/mgs5_new_{i}.jpg" for i in range(1, 11)],
    ],
    "twinsnakes": [
        "test/frame.jpg", "test/twinsnakes_1.jpg", "test/twinsnakes_2.jpg",
        "test/twinsnakes_3.jpg", "test/twinsnakes_4.jpg", "test/twinsnakes_5.jpg",
        *[f"test/new/twinsnakes_new_{i}.jpg" for i in range(1, 11)],
    ],
    "peacewalker": [
        "test/peacewalker_1.jpg", "test/peacewalker_2.jpg", "test/peacewalker_3.jpg",
        "test/peacewalker_4.jpg", "test/peacewalker_5.jpg",
        *[f"test/new/peacewalker_new_{i}.jpg" for i in range(1, 11)],
    ],
}


def preprocess(img, contrast, subtitle_only):
    if subtitle_only:
        w, h = img.size
        img = img.crop((0, int(h * 0.5), w, h))
    img = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)
    img = img.convert("L")
    img = ImageEnhance.Contrast(img).enhance(contrast)
    return img


def ocr_tesseract(pil_image, psm, conf_threshold):
    config = f'--psm {psm} --oem 1 -c "tessedit_char_whitelist={WHITELIST}"'
    data = pytesseract.image_to_data(pil_image, config=config, output_type=pytesseract.Output.DICT)
    words = [data['text'][i] for i in range(len(data['text']))
             if int(data['conf'][i]) >= conf_threshold
             and data['text'][i].strip()
             and data['text'][i].upper() not in EXCLUDE]
    return ' '.join(words)


def ocr_easyocr(pil_image, conf_threshold, reader):
    arr = np.array(pil_image)
    results = reader.readtext(arr)
    words = [text for _, text, conf in results
             if conf >= conf_threshold and text.strip()
             and text.upper() not in EXCLUDE]
    return ' '.join(words)


def run_ocr(pil_image, cfg, reader, conf_override=None):
    conf = conf_override if conf_override is not None else cfg['conf']
    if cfg['engine'] == 'tesseract':
        return ocr_tesseract(pil_image, cfg['psm'], conf)
    else:
        return ocr_easyocr(pil_image, conf, reader)


def word_overlap(a, b):
    a_words = set(a.lower().split())
    b_words = set(b.lower().split())
    if not a_words and not b_words:
        return 1.0
    if not a_words or not b_words:
        return 0.0
    return len(a_words & b_words) / len(a_words | b_words)


if __name__ == '__main__':
    print("Loading EasyOCR model...")
    reader = easyocr.Reader(['en'], verbose=False)
    print("Ready.\n")

    filter_game = sys.argv[1] if len(sys.argv) > 1 else None

    total_correct, total_all = 0, 0

    for game, paths in GAME_MAP.items():
        if filter_game and game != filter_game:
            continue

        cfg = OCR_CONFIG[game]
        print(f"\n{'='*60}")
        print(f"{game} ({cfg['engine']}, contrast={cfg['contrast']}, subtitle_only={cfg['subtitle_only']})")
        print(f"{'='*60}")

        game_correct, game_total = 0, 0

        for path in paths:
            truth = GROUND_TRUTH.get(path)
            if not truth:
                continue
            if not os.path.exists(path):
                print(f"  SKIP {path} (not found)")
                continue

            game_total += 1
            img = Image.open(path)

            # Full image pass for codec detection (low conf)
            full_img = preprocess(img, cfg['contrast'], subtitle_only=False)
            codec_conf = 60 if cfg['engine'] == 'tesseract' else 0.3
            full_text = run_ocr(full_img, cfg, reader, conf_override=codec_conf)
            is_codec = 'PTT' in full_text.upper() and 'TUNE' in full_text.upper()

            # Subtitle pass
            if cfg['subtitle_only']:
                sub_img = preprocess(img, cfg['contrast'], subtitle_only=True)
                sub_text = run_ocr(sub_img, cfg, reader)
            else:
                sub_text = full_text

            expected_type = truth['type']
            expected_text = truth['text']

            if is_codec:
                result, result_text = "CODEC", None
            elif len(sub_text) > 3:
                result, result_text = "TEXT", " ".join(sub_text.split())
            else:
                result, result_text = "NONE", None

            ok = False
            detail = ""
            if expected_type == 'none':
                ok = result == "NONE"
                if not ok:
                    detail = f"got {result}: {result_text or sub_text}"
            elif expected_type == 'codec':
                ok = result == "CODEC"
                if not ok:
                    detail = f"got {result}"
            elif expected_type in ('codec+dialogue', 'dialogue'):
                if result == "TEXT" and expected_text and result_text:
                    score = word_overlap(expected_text, result_text)
                    ok = score > 0.4
                    detail = f"overlap={score:.2f}"
                elif result == "CODEC" and expected_type == 'codec+dialogue':
                    ok = True
                    detail = "codec detected (also valid)"

            status = "OK" if ok else "FAIL"
            if ok:
                game_correct += 1
            filename = os.path.basename(path)
            print(f"  {status:4} {filename:30} expect={expected_type:16} got={result:5} {detail}")
            if result == "TEXT" and result_text:
                print(f"       OCR:   \"{result_text[:80]}\"")
                if expected_text:
                    print(f"       Truth: \"{expected_text[:80]}\"")

        total_correct += game_correct
        total_all += game_total
        print(f"  => {game}: {game_correct}/{game_total}")

    print(f"\n{'='*60}")
    if total_all > 0:
        print(f"TOTAL: {total_correct}/{total_all} ({total_correct/total_all*100:.0f}%)")
    print(f"{'='*60}")
