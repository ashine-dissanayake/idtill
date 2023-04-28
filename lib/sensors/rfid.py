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

def rfid_thread(queue):
    logging.info("Running RFID Thread")
    
    # Create an object of the class MFRC522
    MFRC522Reader = MFRC522(MFRC522_I2C_BUS, MFRC522_SLAVE_ADDR)
    version = MFRC522Reader.getReaderVersion()
    logging.debug(f'MFRC522 Software Version: {version}')

    while True:
        time.sleep(0.25)
        
        try:
            # Scan for cards
            (status, backData, tagType) = MFRC522Reader.scan()

            if status == MFRC522Reader.MIFARE_OK:
                logging.info(f'Card detected, Type: {tagType}')

                # Get UID of the card
                (status, uid, backBits) = MFRC522Reader.identify()
                if status == MFRC522Reader.MIFARE_OK:
                    queue.put(uid)
                    # print(f'Card identified, '
                    #     f'UID: {uid[0]:02x}:{uid[1]:02x}:{uid[2]:02x}:{uid[3]:02x}')
        except: 
            continue                    
  