from lib.ui.thesis_ui import *
from lib.sensors.rfid import rfid_thread
from lib.sensors.pir import pir_thread
from lib.database.database import *

from rpi_backlight import Backlight, BoardType
from queue import Queue

def main(): 
    rfid_to_database_queue = Queue(maxsize = 0)
    database_to_gui_queue = Queue(maxsize = 0)
    gui_to_database_queue = Queue(maxsize = 0)    

    # Start PIR thread
    threading.Thread(target=pir_thread, daemon = True).start()

    # Start RFID thread
    threading.Thread(target=rfid_thread, args = (rfid_to_database_queue,), daemon = True).start()

    # Start Database Thread 
    threading.Thread(target=database_thread, args = (rfid_to_database_queue, database_to_gui_queue, gui_to_database_queue,), daemon = True).start()

    # Start GUI
    app = QtWidgets.QApplication([])
    window = ThesisGUI(database_to_gui_queue, gui_to_database_queue)
    app.lastWindowClosed.connect(close_exec)
    app.exec_()


def close_exec():
    print("Closing IDTILL")
    backlight = Backlight("/sys/class/backlight/1-0045/", BoardType.RASPBERRY_PI)

    if backlight.brightness == 0: 
        backlight.brightness = 80
    
    if backlight.power == False: 
        backlight.power = True
    print("Closing Sequence Complete")


if __name__ == '__main__':  
    main()