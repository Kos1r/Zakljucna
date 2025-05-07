import network
import time
from machine import Pin, SPI
from mfrc522 import MFRC522
import urequests
ssid = "gostje" 
password = "doberdan"

#gostje
#doberdan

wifi = network.WLAN(network.STA_IF)
wifi.active(True)

wifi.connect(ssid, password)

print("Connecting to Wi-Fi...")
while not wifi.isconnected():
    time.sleep(1)
    print(".", end="")

print("\nConnected to Wi-Fi!")
ip_address = wifi.ifconfig()[0]
print("IP address:", ip_address)


# definicije pinou
sda_pin = 5  
sck_pin = 18 
mosi_pin = 23 
miso_pin = 19 
rst_pin = 4   

# Initialize SPI communication
spi = SPI(1, baudrate=1000000, polarity=0, phase=0, sck=Pin(sck_pin), mosi=Pin(mosi_pin), miso=Pin(miso_pin))
rdr = MFRC522(spi=spi, gpioRst=rst_pin, gpioCs=sda_pin)

def scan_rfid():
    print("Place your RFID tag near the reader")

    while True:
        # Request for a card
        status, tag_type = rdr.request(0x26)
        print(status, tag_type)
        if status == rdr.OK:
            print("Card detected!")

            # Read the UID of the card
            status, uid = rdr.anticoll()

            if status == rdr.OK:
                # konverta v lepso oblikso
                
                
                uid_str = ''.join(['{:02X}'.format(x) for x in uid])
                
                klic = urequests.get(f"https://wl0xg7lq-5000.euw.devtunnels.ms/getNFC/{uid_str}")
                print(klic.text)
                print("UID (Hex):", uid_str)
                time.sleep(2)

        time.sleep(1)

#pozene funkcijo
scan_rfid()


