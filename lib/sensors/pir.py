import seeed_python_reterminal.core as rt
import logging
import time
import RPi.GPIO as GPIO
from rpi_backlight import Backlight, BoardType


""" See here for how use things on the reTerminal """
# See https://pypi.org/project/seeed-python-reterminal/ on how to use onboard devices

# PIR CONFIGURATION
PIR_GPIO_PIN = 16

def pir_thread():
    print("Running PIR Thread")
    motion_cnt = 0

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIR_GPIO_PIN, GPIO.IN)

    backlight = Backlight("/sys/class/backlight/1-0045/", BoardType.RASPBERRY_PI)

    last_sense_time = round(time.time() * 1000)
    
    while True:
        if GPIO.input(PIR_GPIO_PIN) == 1:
            motion_cnt += 1

            if backlight.brightness == 0: 
                backlight.brightness = 80
            
            if backlight.power == False: 
                backlight.power = True

            while True:
                if GPIO.input(PIR_GPIO_PIN) == 0:
                    break

            last_sense_time = round(time.time() * 1000)

        curr_sense_time = round(time.time() * 1000)

        if curr_sense_time - last_sense_time == 60000: 
            backlight.brightness = 0
            backlight.power = False
        