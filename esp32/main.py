from mfrc522 import MFRC522
import time

def scan_rfid():
    rdr = MFRC522()

    print("Place your RFID tag near the reader")

    while True:
        (status, tag_type) = rdr.request(rdr.PICC_REQIDL)
        
        if status == rdr.MI_OK:
            print("Card detected!")

            (status, uid) = rdr.anticoll()
            
            if status == rdr.MI_OK:
                print("UID:", uid)
                time.sleep(2) 
        
        time.sleep(1) 

scan_rfid()
