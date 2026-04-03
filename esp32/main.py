import network
import time
from machine import Pin, SPI
from mfrc522 import MFRC522
import urequests

# SEZNAM OMREŽIJ 
wifi_networks = [
    {"ssid": "ASUS_A0_2G", "pass": "kosir234"},
    {"ssid": "gostje", "pass": "doberdan"}
]

# Nastavitev vgrajene lučke (GPIO 2)
vgrajena_led = Pin(2, Pin.OUT)

def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    
    if wifi.isconnected():
        return wifi

    print("Iskanje shranjenih Wi-Fi omrežij...")
    
    for net in wifi_networks:
        print(f"Poskušam se povezati na: {net['ssid']}...")
        wifi.connect(net['ssid'], net['pass'])
        
        # Čakaj 7 sekund na povezavo za vsako omrežje
        attempt = 0
        while not wifi.isconnected() and attempt < 7:
            time.sleep(1)
            print(".", end="")
            attempt += 1
            
        if wifi.isconnected():
            print(f"\nUspešno povezan na {net['ssid']}!")
            print("IP naslov:", wifi.ifconfig()[0])
            
            # Utripni 3x za potrditev uspešne povezave
            for i in range(3):
                vgrajena_led.value(1)
                time.sleep(0.2)
                vgrajena_led.value(0)
                time.sleep(0.2)
            return wifi
        else:
            print(f"\n{net['ssid']} ni na voljo.")
            
    print("Nobeno omrežje ni dosegljivo!")
    return None

# Zaženi povezovanje
wifi_conn = connect_wifi()

# Definicije pinov za RFID
sda_pin = 5  
sck_pin = 18 
mosi_pin = 23 
miso_pin = 19 
rst_pin = 4   

# Initialize SPI communication
spi = SPI(1, baudrate=1000000, polarity=0, phase=0, sck=Pin(sck_pin), mosi=Pin(mosi_pin), miso=Pin(miso_pin))
rdr = MFRC522(spi=spi, gpioRst=rst_pin, gpioCs=sda_pin)

def scan_rfid():
    #checks if we r connected
    if not network.WLAN(network.STA_IF).isconnected():
        print("Naprava ni povezana na internet. Skeniranje onemogočeno.")
        return

    print("Place your RFID tag near the reader")

    while True:
        status, tag_type = rdr.request(0x26)
        
        if status == rdr.OK:
            status, uid = rdr.anticoll()

            if status == rdr.OK:
                vgrajena_led.value(1)
                
                uid_str = ''.join(['{:02X}'.format(x) for x in uid])
                print("Card detected! UID (Hex):", uid_str)
                
                try:
                    klic = urequests.get(f"https://044ttxm2-5000.euw.devtunnels.ms/getNFC/{uid_str}")
                    print("Server response:", klic.text)
                except Exception as e:
                    print("Network error:", e)

                time.sleep(1)
                vgrajena_led.value(0)
                time.sleep(1)

        time.sleep(0.1)

# Pozene funkcijo samo če je wifi povezan
if wifi_conn:
    scan_rfid()