from atproto import Client
from credentialsbsky import *
import cv2
import random
import time
import os
import traceback


client = Client()
client.login('randommetalgear.bsky.social', app_password)

# Load video files and frame counts
games = [
    (cv2.VideoCapture('mgs1.mp4'), "1"),
    (cv2.VideoCapture('mgs2.mp4'), " 2"),
    (cv2.VideoCapture('mgs3.mp4'), " 3"),
    (cv2.VideoCapture('mgs4.mp4'), " 4"),
    (cv2.VideoCapture('mgs5.mp4'), " 5"),
    (cv2.VideoCapture('twinsnakes.mp4'), ": The Twin Snakes"),
    (cv2.VideoCapture('peacewalker.mp4'), ": Peace Walker"),
]
games = [(cap, int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), name) for cap, name in games]


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

    try:
        with open('output.jpg', 'rb') as f:
            img_data = f.read()
        last_post = client.send_image(text='', image=img_data, image_alt='A screenshot from Metal Gear Solid' + which_mgs)
        print(time.strftime("%I:%M:%S") + ": Skeeted! Waiting...")
        print(last_post.uri)
        time.sleep(random.randint(1800, 2700))
    except Exception:
        print(time.strftime("%I:%M:%S") + ": Uh oh, error posting skeet, recycling in 30s...")
        traceback.print_exc()
        time.sleep(30)

    if os.path.exists("output.jpg"):
        os.remove("output.jpg")