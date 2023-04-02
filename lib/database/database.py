import pandas  as pd
import os

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


def database_thread(uid_queue, gui_queue):
    """
    This is a database thread.
    """
    df = pd.read_csv(f'{os.getcwd()}/database/tag.csv')

    while True: 
        uid = uid_queue.get() # list format
        uid_str = uid_hex_format(uid)
        ind = list(df['uid'][df['uid'] == uid_str].index)
        uid_info = df.iloc[ind].values.flatten().tolist()

        if len(ind) == 1:
            packet = ind + uid_info 
        elif len(ind) < 1: 
            packet = [-1, "UNKNOWN", "UNKNOWN", "unknown.mp4", "unknown.png"]
        elif len(ind) > 1:
            packet = [-1, uid_info[0], "DUPLICATE", "duplicate.mp4", "duplicate.png"]

        gui_queue.put(packet)