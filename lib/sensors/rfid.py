import time
import logging
import seeed_python_reterminal.core as rt
from mfrc522_i2c import MFRC522

""" See here for how use things on the reTerminal """
# See https://pypi.org/project/seeed-python-reterminal/ on how to use onboard devices

""" See this REPO For RFID Examples """
# https://github.com/cpranzl/mfrc522_i2c

# MFRC522 Configuration
MFRC522_I2C_BUS = 0x00
MFRC522_SLAVE_ADDR = 0x28


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


def rfid_thread(queue):
    logging.info("Running RFID Thread")
    
    # Create an object of the class MFRC522
    MFRC522Reader = MFRC522(MFRC522_I2C_BUS, MFRC522_SLAVE_ADDR)
    version = MFRC522Reader.getReaderVersion()
    logging.debug(f'MFRC522 Software Version: {version}')

    while True:
        # Scan for cards
        time.sleep(0.25)
        
        try:
            (status, backData, tagType) = MFRC522Reader.scan()

            if status == MFRC522Reader.MIFARE_OK:
                logging.info(f'Card detected, Type: {tagType}')

                # Get UID of the card
                (status, uid, backBits) = MFRC522Reader.identify()
                if status == MFRC522Reader.MIFARE_OK:
                    queue.put(uid_hex_format(uid))

        except: 
            continue                    
  