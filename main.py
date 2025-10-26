from credentials import *
import tweepy
import cv2
import random
import time
import os
from pathlib import Path


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#import video files
mgs1 = cv2.VideoCapture('mgs1.mp4')
mgs2 = cv2.VideoCapture('mgs2.mp4')
mgs3 = cv2.VideoCapture('mgs3.mp4')

#get number of frames in each file
mgs1_num_frames = int(mgs1.get(cv2.CAP_PROP_FRAME_COUNT))
mgs2_num_frames = int(mgs2.get(cv2.CAP_PROP_FRAME_COUNT))
mgs3_num_frames = int(mgs3.get(cv2.CAP_PROP_FRAME_COUNT))


while 1:
    #choose an MGS game
    choose_mgs = random.randint(1,3 )
    print("Game chosen: MGS" + str(choose_mgs))

    if choose_mgs==1:                                     #The following repeats for each MGS below
        mgs1_frame_id = random.randint(0,mgs1_num_frames) #get a random frame ID from this file
        mgs1.set(cv2.CAP_PROP_POS_FRAMES, mgs1_frame_id)  #set current opencv frame to the random frame number
        success,image = mgs1.read()                       #read the random frame number from file
        if success:
            cv2.imwrite("output.jpg", image)              #write the random frame number to output.jpeg
    elif choose_mgs==2:
        mgs2_frame_id = random.randint(0,mgs2_num_frames)
        mgs2.set(cv2.CAP_PROP_POS_FRAMES, mgs2_frame_id)
        success,image = mgs2.read()
        if success:
            cv2.imwrite("output.jpg", image)
    elif choose_mgs==3:
        mgs3_frame_id = random.randint(0,mgs3_num_frames)
        mgs3.set(cv2.CAP_PROP_POS_FRAMES, mgs3_frame_id)
        success,image = mgs3.read()
        if success:
            cv2.imwrite("output.jpg", image)
    try: # send tweet, then wait 30 minutes
        media = api.media_upload("output.jpg")                                  #new twitter/tweepy api - upload the file and get a media ID
        print(time.strftime("%I:%M:%S") + ": Media ID string - " + media.media_id_string)
        tweet = api.update_status(status="", media_ids=[media.media_id_string]) #update a status with the media id, had to send as array of 1 to avoid a too many media ids error 
        print(time.strftime("%I:%M:%S") + ": Tweeted! Waiting...")
        time.sleep(random.randint(1800,2700))                                   #Wait sometime between 30 to 45 min
    except Exception: # error sending tweet, wait 30s to try a new gif     
        print(time.strftime("%I:%M:%S") + ": Uh oh, error posting tweet, recycling in 30s...")
        time.sleep(30)

    if os.path.exists("output.jpg") == True:
        print("Deleting last tweeted image from local machine")
        os.remove("output.jpg") 