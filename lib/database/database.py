import pandas  as pd
import os
from lib.state.state import *
import random
import time 

TOTAL_TEST_QUESTIONS = 15
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
        uid_str += hex(byte).split('x')[-1] + ":"

    return uid_str[:-1]    


def create_test_set(db): 
    test_set = []

    for i in range(TOTAL_TEST_QUESTIONS):
        ind = random.randint(0, len(db) - 1) # Exclude end point

        char = db.iloc[ind].values[1]
        correct_answer = db.iloc[ind].values[2] 
        options = [correct_answer]

        for j in range(OPTIONS_PER_QUESTIONS - 1): 
            option_ind = random.randint(0, len(db) - 1) # Exclude end point
            options.append(db.iloc[option_ind].values[2])
        
        random.shuffle(options)
        test_set.append([char] + options + [options.index(correct_answer) + 1])

    return test_set


def database_thread(from_rfid_queue, to_gui_queue, from_gui_queue):
    """
    This is a database thread.
    """
    df = pd.read_csv(f'{os.getcwd()}/database/hiragana.csv')
    curr_state = State.LEARN
    time.sleep(1)

    while True: 

        # Check if state changed. 
        if not from_gui_queue.empty():
            curr_state = from_gui_queue.get()
            if curr_state == State.TEST: 
                test_set = create_test_set(df)
                to_gui_queue.put(test_set)
            print(curr_state)
        
        if not from_rfid_queue.empty():
            uid = from_rfid_queue.get() # list format
            uid_str = uid_hex_format(uid)
            ind = list(df['uid'][df['uid'] == uid_str].index)
            uid_info = df.iloc[ind].values.flatten().tolist()

            if len(ind) == 1:
                packet = ind + uid_info 
            elif len(ind) < 1: 
                packet = [-1, "UNKNOWN", "UNKNOWN", "unknown.mp4", "unknown.png"]
            elif len(ind) > 1:
                packet = [-1, uid_info[0], "DUPLICATE", "duplicate.mp4", "duplicate.png"]

            to_gui_queue.put(packet)