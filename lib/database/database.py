import pandas  as pd
import os
from lib.state.state import *
import random
import time 
import numpy as np

MAX_TEST_QUESTIONS = 15
OPTIONS_PER_QUESTIONS = 3

def uid_hex_format(uid : list): 
    """
    Returns hex forat of uid. 

    param: 
        uid (list) list format of uid

    return: 
        hex format of uid
    """
    uid_str = ""
    for byte in uid: 
        uid_str += hex(byte).split('x')[-1].zfill(2) + ":"

    return uid_str[:-1]    


def create_test_set(db): 
    test_set = []
    total_questions = MAX_TEST_QUESTIONS 

    if len(db) < MAX_TEST_QUESTIONS: 
        total_questions = len(db)
    print(total_questions)
    for i in range(total_questions):
        ind = random.randint(0, len(db) - 1) # Exclude end point

        char = db.iloc[ind].values[1]
        correct_answer = db.iloc[ind].values[2] 
        options = [correct_answer]

        for j in range(OPTIONS_PER_QUESTIONS - 1): 
            option_ind = random.randint(0, len(db) - 1) # Exclude end point

            while db.iloc[option_ind].values[2] in options: 
                option_ind = random.randint(0, len(db) - 1)

            options.append(db.iloc[option_ind].values[2])
        
        random.shuffle(options)
        test_set.append([char] + options + [options.index(correct_answer) + 1])

    return test_set


def media_exist(uid_info, ind):
    if pd.isnull(uid_info[3]): # folder not provided
        print("Missing Folder")
        return [-1, "MISSING MEDIA", "MISSING MEDIA", "MISSING MEDIA", "missing_media", "missing_media.mp4", "missing_media.png"]
    
    folder_path = f'{os.getcwd()}/database/{uid_info[3]}/'

    if os.path.exists(folder_path): # folder does exist 
        if os.path.isfile(folder_path + uid_info[4]) != True or os.path.isfile(folder_path + uid_info[5]) != True:
            print("Missing Video")
            uid_info[3] = "missing_media"
            uid_info[4] = 'missing_media.mp4'
            uid_info[5] = 'missing_media.png' 
            ind = -1
    else: 
        print("Missing Both")
        uid_info[3] = "missing_media"
        uid_info[4] = 'missing_media.mp4'
        uid_info[5] = 'missing_media.png'
        ind = -1

    return [ind] + uid_info


def database_thread(from_rfid_queue, to_gui_queue, from_gui_queue):
    """
    This is a database thread.
    """
    df = pd.read_csv(f'{os.getcwd()}/database/tag.csv')
    curr_state = State.LEARN
    time.sleep(1)

    while True: 

        # Check if state changed. 
        if not from_gui_queue.empty():
            curr_state = from_gui_queue.get()
            if curr_state == State.TEST: 
                test_set = create_test_set(df)
                to_gui_queue.put(test_set)
        
        if not from_rfid_queue.empty():
            if curr_state == State.TEST: # No cards should be scanned here. 
                from_rfid_queue.clear()
            else: 
                uid = from_rfid_queue.get() # list format
                uid_str = uid_hex_format(uid)
                ind = list(df['uid'][df['uid'] == uid_str].index)
                uid_info = df.iloc[ind].values.flatten().tolist() # [column, uid, char, english, folder, video, image]

                print(uid_info)
                if len(ind) == 1:
                    packet = media_exist(uid_info, ind)
                elif len(ind) < 1: 
                    packet = [-1, uid_str, "UNKNOWN", "UNKNOWN", "unknown", "unknown.mp4", "unknown.png"]
                elif len(ind) > 1:
                    packet = [-1, uid_str, "DUPLICATE", "DUPLICATE", "duplicate", "duplicate.mp4", "duplicate.png"]

                to_gui_queue.put(packet)