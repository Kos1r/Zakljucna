import network
import time

ssid = "ASUS_A0_2G" 
password = "kosir234"

wifi = network.WLAN(network.STA_IF)
wifi.active(True)

wifi.connect(ssid, password)

print("Connecting to Wi-Fi...")
while not wifi.isconnected():
    time.sleep(1)
    print(".", end="")

print("\nConnected to Wi-Fi!")
print("Network config:", wifi.ifconfig())
