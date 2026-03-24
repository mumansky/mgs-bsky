#!/usr/bin/env python3
"""Extract 10 random frames per game for extended test suite."""
import cv2
import os
import random

random.seed(42)

OUTPUT_DIR = 'test/new'
os.makedirs(OUTPUT_DIR, exist_ok=True)

GAMES = {
    'mgs1':        'mgs1.mp4',
    'mgs2':        'mgs2.mp4',
    'mgs3':        'mgs3.mp4',
    'mgs4':        'mgs4.mp4',
    'mgs5':        'mgs5.mp4',
    'twinsnakes':  'twinsnakes.mp4',
    'peacewalker': 'peacewalker.mp4',
}

for game, video_file in GAMES.items():
    cap = cv2.VideoCapture(video_file)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frames = sorted(random.sample(range(total), 10))
    print(f"{game}: {total} frames, extracting {frames}")
    for i, frame_id in enumerate(frames):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        ok, img = cap.read()
        if ok:
            path = os.path.join(OUTPUT_DIR, f'{game}_new_{i+1}.jpg')
            cv2.imwrite(path, img)
            print(f"  saved {path}")
    cap.release()

print("\nDone.")
