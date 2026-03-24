from atproto import Client
from credentialsbsky import *
import cv2
import random
import time
import os
import traceback
import numpy as np
import pytesseract
import easyocr
from PIL import Image, ImageEnhance


WHITELIST = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,!?' -"
EXCLUDE = {'NRM'}

# Per-game OCR configs (tuned via tune.py)
OCR_CONFIG = {
    " 1":                {"engine": "tesseract", "contrast": 2.0, "psm": 6,  "conf": 60,  "subtitle_only": True},
    " 2":                {"engine": "tesseract", "contrast": 2.0, "psm": 11, "conf": 90,  "subtitle_only": True},
    " 3":                {"engine": "easyocr",   "contrast": 2.5, "conf": 0.6, "subtitle_only": False},
    " 4":                {"engine": "easyocr",   "contrast": 2.5, "conf": 0.75, "subtitle_only": True},
    " 5":                {"engine": "easyocr",   "contrast": 2.0, "conf": 0.8, "subtitle_only": True},
    ": The Twin Snakes": {"engine": "tesseract", "contrast": 2.0, "psm": 6,  "conf": 80,  "subtitle_only": True},
    ": Peace Walker":    {"engine": "easyocr",   "contrast": 2.5, "conf": 0.55, "subtitle_only": False},
}

client = Client()
client.login('randommetalgear.bsky.social', app_password)

# Load video files and frame counts
games = [
    (cv2.VideoCapture('mgs1.mp4'), " 1"),
    (cv2.VideoCapture('mgs2.mp4'), " 2"),
    (cv2.VideoCapture('mgs3.mp4'), " 3"),
    (cv2.VideoCapture('mgs4.mp4'), " 4"),
    (cv2.VideoCapture('mgs5.mp4'), " 5"),
    (cv2.VideoCapture('twinsnakes.mp4'), ": The Twin Snakes"),
    (cv2.VideoCapture('peacewalker.mp4'), ": Peace Walker"),
]
games = [(cap, int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), name) for cap, name in games]

print("Loading EasyOCR model...")
easyocr_reader = easyocr.Reader(['en'], verbose=False)
print("Ready.")


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
    words = []
    for i in range(len(data['text'])):
        word = data['text'][i]
        conf = int(data['conf'][i])
        if word.strip() and word.upper() not in EXCLUDE:
            marker = "+" if conf >= conf_threshold else "-"
            print(f"  [{marker} {conf:3}%] {word}")
            if conf >= conf_threshold:
                words.append(word)
    return ' '.join(words)


def ocr_easyocr(pil_image, conf_threshold):
    arr = np.array(pil_image)
    results = easyocr_reader.readtext(arr)
    words = []
    for _, text, conf in results:
        if text.strip() and text.upper() not in EXCLUDE:
            marker = "+" if conf >= conf_threshold else "-"
            print(f"  [{marker} {conf*100:5.1f}%] {text}")
            if conf >= conf_threshold:
                words.append(text)
    return ' '.join(words)


def run_ocr(pil_image, cfg, conf_override=None):
    conf = conf_override if conf_override is not None else cfg['conf']
    if cfg['engine'] == 'tesseract':
        return ocr_tesseract(pil_image, cfg['psm'], conf)
    else:
        return ocr_easyocr(pil_image, conf)


while True:
    cap, num_frames, which_mgs = random.choice(games)
    frame_id = random.randint(0, num_frames - 1)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
    success, image = cap.read()

    if not success:
        print("Failed to read frame, retrying in 30s...")
        time.sleep(30)
        continue

    cv2.imwrite("output.jpg", image)
    print("Game chosen: Metal Gear Solid" + which_mgs)

    original = Image.open("output.jpg")
    cfg = OCR_CONFIG[which_mgs]
    print(f"  OCR: {cfg['engine']}, contrast={cfg['contrast']}, subtitle_only={cfg['subtitle_only']}")

    # Full image OCR for codec detection (low conf to catch PTT/TUNE)
    print("  --- full image ---")
    full_img = preprocess(original, cfg['contrast'], subtitle_only=False)
    codec_conf = 60 if cfg['engine'] == 'tesseract' else 0.3
    full_text = run_ocr(full_img, cfg, conf_override=codec_conf)
    is_codec = 'PTT' in full_text.upper() and 'TUNE' in full_text.upper()

    # Subtitle text (crop if configured)
    if cfg['subtitle_only']:
        print("  --- subtitle crop ---")
        sub_img = preprocess(original, cfg['contrast'], subtitle_only=True)
        sub_text = run_ocr(sub_img, cfg)
    else:
        sub_text = full_text

    # Build alt text
    if is_codec:
        alt_text = f'A codec call screen from Metal Gear Solid{which_mgs}'
    elif len(sub_text) > 3:
        cleaned = " ".join(sub_text.split())
        truncated = cleaned[:500] + ("..." if len(cleaned) > 500 else "")
        alt_text = f'A screenshot from Metal Gear Solid{which_mgs}.\nOn-screen text reads: "{truncated}"'
    else:
        alt_text = f'A screenshot from Metal Gear Solid{which_mgs}'
    print(f"Alt text: {alt_text}")

    try:
        with open('output.jpg', 'rb') as f:
            img_data = f.read()
        last_post = client.send_image(text='', image=img_data, image_alt=alt_text)
        print(time.strftime("%I:%M:%S") + ": Skeeted! Waiting...")
        print(last_post.uri)
        time.sleep(random.randint(1800, 2700))
    except Exception:
        print(time.strftime("%I:%M:%S") + ": Uh oh, error posting skeet, recycling in 30s...")
        traceback.print_exc()
        time.sleep(30)

    if os.path.exists("output.jpg"):
        os.remove("output.jpg")
