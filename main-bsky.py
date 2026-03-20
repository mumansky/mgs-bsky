from atproto import Client
from credentialsbsky import *
from pathlib import Path
import cv2
import random
import time
import os
import sqlite3
import traceback


client = Client()
client.login('randommetalgear.bsky.social', app_password)

#con = sqlite3.connect("mgs.db")
#cur = con.cursor()
#cur.execute("CREATE TABLE mgs_posts(uri, num_likes, num_reposts)")


#import video files
mgs1 = cv2.VideoCapture('mgs1.mp4')
mgs2 = cv2.VideoCapture('mgs2.mp4')
mgs3 = cv2.VideoCapture('mgs3.mp4')
mgs4 = cv2.VideoCapture('mgs4.mp4')
mgs5 = cv2.VideoCapture('mgs5.mp4')
twinsnakes = cv2.VideoCapture('twinsnakes.mp4')
peacewalker = cv2.VideoCapture('peacewalker.mp4')

#get number of frames in each file
mgs1_num_frames = int(mgs1.get(cv2.CAP_PROP_FRAME_COUNT))
mgs2_num_frames = int(mgs2.get(cv2.CAP_PROP_FRAME_COUNT))
mgs3_num_frames = int(mgs3.get(cv2.CAP_PROP_FRAME_COUNT))
mgs4_num_frames = int(mgs4.get(cv2.CAP_PROP_FRAME_COUNT))
mgs5_num_frames = int(mgs5.get(cv2.CAP_PROP_FRAME_COUNT))
twinsnakes_num_frames = int(twinsnakes.get(cv2.CAP_PROP_FRAME_COUNT))
peacewalker_num_frames = int(peacewalker.get(cv2.CAP_PROP_FRAME_COUNT))



while 1:
    #choose an MGS game
    choose_mgs = random.randint(1,7)

    if choose_mgs==1:                                     #The following repeats for each MGS below
        mgs1_frame_id = random.randint(0,mgs1_num_frames) #get a random frame ID from this file
        mgs1.set(cv2.CAP_PROP_POS_FRAMES, mgs1_frame_id)  #set current opencv frame to the random frame number
        success,image = mgs1.read()                       #read the random frame number from file
        if success:
            cv2.imwrite("output.jpg", image)              #write the random frame number to output.jpeg
            which_mgs = "1"
    elif choose_mgs==2:
        mgs2_frame_id = random.randint(0,mgs2_num_frames)
        mgs2.set(cv2.CAP_PROP_POS_FRAMES, mgs2_frame_id)
        success,image = mgs2.read()
        if success:
            cv2.imwrite("output.jpg", image)
            which_mgs = " 2"
    elif choose_mgs==3:
        mgs3_frame_id = random.randint(0,mgs3_num_frames)
        mgs3.set(cv2.CAP_PROP_POS_FRAMES, mgs3_frame_id)
        success,image = mgs3.read()
        if success:
            cv2.imwrite("output.jpg", image)
            which_mgs = " 3"
    elif choose_mgs==4:
        mgs4_frame_id = random.randint(0,mgs4_num_frames)
        mgs4.set(cv2.CAP_PROP_POS_FRAMES, mgs4_frame_id)
        success,image = mgs4.read()
        if success:
            cv2.imwrite("output.jpg", image)
            which_mgs = " 4"
    elif choose_mgs==5:
        mgs5_frame_id = random.randint(0,mgs5_num_frames)
        mgs5.set(cv2.CAP_PROP_POS_FRAMES, mgs5_frame_id)
        success,image = mgs5.read()
        if success:
            cv2.imwrite("output.jpg", image)
            which_mgs = " 5"
    elif choose_mgs==6:
        ts_frame_id = random.randint(0,twinsnakes_num_frames)
        twinsnakes.set(cv2.CAP_PROP_POS_FRAMES, ts_frame_id)
        success,image = twinsnakes.read()
        if success:
            cv2.imwrite("output.jpg", image)
            which_mgs = ": The Twin Snakes"
    elif choose_mgs==7:
        pw_frame_id = random.randint(0,peacewalker_num_frames)
        peacewalker.set(cv2.CAP_PROP_POS_FRAMES, pw_frame_id)
        success,image = peacewalker.read()
        if success:
            cv2.imwrite("output.jpg", image)
            which_mgs = ": Peace Walker"

    print("Game chosen: Metal Gear Solid" + which_mgs)
    
    try: # send skeet, then wait 30 minutes
        with open('output.jpg','rb') as f:
            img_data = f.read()
        last_post = client.send_image(text='', image=img_data, image_alt='A screenshot from Metal Gear Solid' + which_mgs)
        print(time.strftime("%I:%M:%S") + ": Skeeted! Waiting...")
        print(last_post.uri)
        
        #sql_data = [last_post.uri,0,0]
        #cur.executemany("INSERT INTO mgs_posts VALUES (?,?,?)",(sql_data,))
        #con.commit()
        
        time.sleep(random.randint(1800,2700))                                   #Wait sometime between 30 to 45 min
    except Exception: # error sending skeet, wait 30s to try a new gif     
        print(time.strftime("%I:%M:%S") + ": Uh oh, error posting skeet, recycling in 30s...")
        traceback.print_exc()
        time.sleep(30)

    if os.path.exists("output.jpg") == True:
        print("Deleting last tweeted image from local machine")
        os.remove("output.jpg")
    else:
        print("No output.jpg found")