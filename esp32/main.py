from mfrc522 import MFRC522
import time

def scan_rfid():
    rdr = MFRC522()

    print("Place your RFID tag near the reader")

    while True:
        # Scan for cards
        (status, tag_type) = rdr.request(rdr.PICC_REQIDL)
        
        if status == rdr.MI_OK:
            print("Card detected!")

            # Get the UID of the card
            (status, uid) = rdr.anticoll()
            
            if status == rdr.MI_OK:
                print("UID:", uid)
                time.sleep(2)  # Wait a bit before scanning again
        
        time.sleep(1)  # Wait for a second before scanning again

# Run the RFID scan
scan_rfid()
