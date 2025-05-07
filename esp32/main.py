from machine import Pin, SPI
from mfrc522 import MFRC522
import time

# definicije pinou
sda_pin = 5  
sck_pin = 18 
mosi_pin = 23 
miso_pin = 19 
rst_pin = 4   

#SPI komunikacija
spi = SPI(1, baudrate=1000000, polarity=0, phase=0, sck=Pin(sck_pin), mosi=Pin(mosi_pin), miso=Pin(miso_pin))
rdr = MFRC522(spi=spi, gpioRst=rst_pin, gpioCs=sda_pin)

def scan_rfid():
    print("Place your RFID tag near the reader")

    while True:
        # Request for a card
        status, tag_type = rdr.request(0x26)

        if status == rdr.OK:
            print("Card detected!")

            # UID
            status, uid = rdr.anticoll()

            if status == rdr.OK:
                # konverta v lepso oblikso
                uid_str = ''.join(['{:02X}'.format(x) for x in uid])
                print("UID (Hex):", uid_str)
                time.sleep(2)

        time.sleep(1)

scan_rfid()

