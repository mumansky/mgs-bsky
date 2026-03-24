#!/usr/bin/env python3
# Automated OCR parameter tuner. Tunes each game independently.
import sys
import os
import itertools
from multiprocessing import Pool, cpu_count
import pytesseract
import easyocr
import cv2
import numpy as np
from PIL import Image, ImageEnhance

sys.path.insert(0, 'test')
from ground_truth import GROUND_TRUTH

TEST_DIR = 'test'
EXCLUDE = {'NRM'}
WHITELIST = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,!?' -"

# Map filenames to games
GAME_MAP = {
    "mgs1": ["mgs1.jpg", "mgs1_1.jpg", "mgs1_2.jpg", "mgs1_3.jpg", "mgs1_4.jpg", "mgs1_5.jpg"],
    "mgs2": ["mgs2.jpg", "codec.webp", "mgs2_1.jpg", "mgs2_2.jpg", "mgs2_3.jpg", "mgs2_4.jpg", "mgs2_5.jpg"],
    "mgs3": ["mgs3.jpg", "mgs3_1.jpg", "mgs3_2.jpg", "mgs3_3.jpg", "mgs3_4.jpg", "mgs3_5.jpg"],
    "mgs4": ["near.webp", "mgs4_1.jpg", "mgs4_2.jpg", "mgs4_3.jpg", "mgs4_4.jpg", "mgs4_5.jpg"],
    "mgs5": ["mgs5_1.jpg", "mgs5_2.jpg", "mgs5_3.jpg", "mgs5_4.jpg", "mgs5_5.jpg"],
    "twinsnakes": ["frame.jpg", "twinsnakes_1.jpg", "twinsnakes_2.jpg", "twinsnakes_3.jpg", "twinsnakes_4.jpg", "twinsnakes_5.jpg"],
    "peacewalker": ["peacewalker_1.jpg", "peacewalker_2.jpg", "peacewalker_3.jpg", "peacewalker_4.jpg", "peacewalker_5.jpg"],
}


def word_overlap(a, b):
    a_words = set(a.lower().split())
    b_words = set(b.lower().split())
    if not a_words and not b_words:
        return 1.0
    if not a_words or not b_words:
        return 0.0
    return len(a_words & b_words) / len(a_words | b_words)


def preprocess(img, contrast, use_clahe, subtitle_only):
    if subtitle_only:
        w, h = img.size
        img = img.crop((0, int(h * 0.5), w, h))
    img = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)
    if use_clahe:
        arr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        arr = clahe.apply(arr)
        arr = cv2.adaptiveThreshold(arr, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        return Image.fromarray(arr)
    else:
        img = img.convert("L")
        img = ImageEnhance.Contrast(img).enhance(contrast)
        return img


def run_ocr(pil_image, psm, conf_threshold):
    config = f'--psm {psm} --oem 1 -c "tessedit_char_whitelist={WHITELIST}"'
    data = pytesseract.image_to_data(pil_image, config=config, output_type=pytesseract.Output.DICT)
    words = [data['text'][i] for i in range(len(data['text']))
             if int(data['conf'][i]) >= conf_threshold
             and data['text'][i].strip()
             and data['text'][i].upper() not in EXCLUDE]
    return ' '.join(words)


def score_one(params):
    game, contrast, use_clahe, subtitle_only, psm, conf_threshold = params
    filenames = GAME_MAP[game]
    total, correct, text_score = 0, 0, 0.0

    for filename in filenames:
        truth = GROUND_TRUTH.get(filename)
        if not truth:
            continue
        path = os.path.join(TEST_DIR, filename)
        if not os.path.exists(path):
            continue
        total += 1
        img = Image.open(path)

        full_img = preprocess(img, contrast, use_clahe, subtitle_only=False)
        full_text = run_ocr(full_img, psm, conf_threshold)
        is_codec = 'PTT' in full_text.upper() and 'TUNE' in full_text.upper()

        sub_img = preprocess(img, contrast, use_clahe, subtitle_only=True)
        sub_text = run_ocr(sub_img, psm, conf_threshold)

        expected_type = truth['type']
        expected_text = truth['text']

        if expected_type == 'none':
            produced_text = sub_text if len(sub_text) > 3 else ''
            if not produced_text and not is_codec:
                correct += 1
                text_score += 1.0
        elif expected_type == 'codec':
            if is_codec:
                correct += 1
                text_score += 1.0
        elif expected_type in ('codec+dialogue', 'dialogue'):
            if expected_text and len(sub_text) > 3:
                score = word_overlap(expected_text, sub_text)
                text_score += score
                if score > 0.4:
                    correct += 1

    return params, correct, total, text_score / total if total else 0


# Parameter grid
contrasts = [1.5, 2.0, 2.5, 3.0]
clahe_options = [False, True]
subtitle_options = [False, True]
psm_modes = [6, 11]
conf_thresholds = [60, 70, 75, 80, 85, 90]

base_combos = list(itertools.product(contrasts, clahe_options, subtitle_options, psm_modes, conf_thresholds))
base_combos = [(c, cl, s, p, t) for c, cl, s, p, t in base_combos if not (cl and c != contrasts[0])]

if __name__ == '__main__':
    num_workers = cpu_count()

    for game in GAME_MAP:
        combos = [(game, c, cl, s, p, t) for c, cl, s, p, t in base_combos]
        num_images = len([f for f in GAME_MAP[game] if f in GROUND_TRUTH and os.path.exists(os.path.join(TEST_DIR, f))])
        print(f"\n{'='*60}")
        print(f"TUNING: {game} ({num_images} images, {len(combos)} combos, {num_workers} workers)")
        print(f"{'='*60}", flush=True)

        results = []
        with Pool(num_workers) as pool:
            for i, result in enumerate(pool.imap_unordered(score_one, combos)):
                params, correct, total, avg_score = result
                _, contrast, use_clahe, subtitle_only, psm, conf_threshold = params
                results.append((avg_score, correct, total, contrast, use_clahe, subtitle_only, psm, conf_threshold))
                if (i + 1) % 10 == 0 or i + 1 == len(combos):
                    print(f"  [{i+1}/{len(combos)}] done...", flush=True)

        results.sort(reverse=True)
        print(f"\n  TOP 3 Tesseract for {game}:")
        for avg_score, correct, total, contrast, use_clahe, subtitle_only, psm, conf_threshold in results[:3]:
            print(f"    score={avg_score:.3f} ({correct}/{total}) | contrast={contrast} clahe={use_clahe} subtitle_only={subtitle_only} psm={psm} conf={conf_threshold}%")

    # --- EasyOCR tuning ---
    print(f"\n{'='*60}")
    print(f"Loading EasyOCR model...")
    print(f"{'='*60}", flush=True)
    reader = easyocr.Reader(['en'], verbose=False)

    def run_easyocr(image_path, conf_threshold):
        results = reader.readtext(image_path)
        words = [text for _, text, conf in results
                 if conf >= conf_threshold and text.strip()
                 and text.upper() not in EXCLUDE]
        return ' '.join(words)

    easy_contrasts = [1.0, 1.5, 2.0, 2.5]
    easy_conf_thresholds = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

    for game in GAME_MAP:
        filenames = GAME_MAP[game]
        easy_combos = list(itertools.product(easy_contrasts, [False, True], easy_conf_thresholds))
        num_images = len([f for f in filenames if f in GROUND_TRUTH and os.path.exists(os.path.join(TEST_DIR, f))])
        print(f"\n{'='*60}")
        print(f"EASYOCR TUNING: {game} ({num_images} images, {len(easy_combos)} combos)")
        print(f"{'='*60}", flush=True)

        results = []
        for ci, (contrast, subtitle_only, conf_threshold) in enumerate(easy_combos):
            total, correct, text_score = 0, 0, 0.0

            for filename in filenames:
                truth = GROUND_TRUTH.get(filename)
                if not truth:
                    continue
                path = os.path.join(TEST_DIR, filename)
                if not os.path.exists(path):
                    continue
                total += 1
                img = Image.open(path)

                # Preprocess for EasyOCR (save temp file since readtext takes path or numpy)
                proc_img = preprocess(img, contrast, False, subtitle_only)
                arr = np.array(proc_img)

                easy_results = reader.readtext(arr)
                words = [text for _, text, conf in easy_results
                         if conf >= conf_threshold and text.strip()
                         and text.upper() not in EXCLUDE]
                ocr_text = ' '.join(words)

                # Codec detection on full image
                full_img = preprocess(img, contrast, False, subtitle_only=False)
                full_arr = np.array(full_img)
                full_results = reader.readtext(full_arr)
                full_text = ' '.join(text for _, text, _ in full_results)
                is_codec = 'PTT' in full_text.upper() and 'TUNE' in full_text.upper()

                expected_type = truth['type']
                expected_text = truth['text']

                if expected_type == 'none':
                    produced = ocr_text if len(ocr_text) > 3 else ''
                    if not produced and not is_codec:
                        correct += 1
                        text_score += 1.0
                elif expected_type == 'codec':
                    if is_codec:
                        correct += 1
                        text_score += 1.0
                elif expected_type in ('codec+dialogue', 'dialogue'):
                    if expected_text and len(ocr_text) > 3:
                        score = word_overlap(expected_text, ocr_text)
                        text_score += score
                        if score > 0.4:
                            correct += 1

            avg_score = text_score / total if total else 0
            results.append((avg_score, correct, total, contrast, subtitle_only, conf_threshold))
            if (ci + 1) % 6 == 0 or ci + 1 == len(easy_combos):
                print(f"  [{ci+1}/{len(easy_combos)}] done...", flush=True)

        results.sort(reverse=True)
        print(f"\n  TOP 3 EasyOCR for {game}:")
        for avg_score, correct, total, contrast, subtitle_only, conf_threshold in results[:3]:
            print(f"    score={avg_score:.3f} ({correct}/{total}) | contrast={contrast} subtitle_only={subtitle_only} conf={conf_threshold}")
