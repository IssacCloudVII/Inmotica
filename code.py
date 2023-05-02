from machine import Pin
import time
relay_pin_2 = Pin(2, Pin.OUT)
while True:
	relay_pin_2.value(1)
	time.sleep(0.5)
	relay_pin_2.value(0)
	time.sleep(0.5)