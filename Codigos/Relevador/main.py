import machine
import time

relay_pin = machine.Pin(4, machine.Pin.OUT)

while True:
    relay_pin.value(1)  # turn the relay on
    time.sleep(1)        # wait for 1 second
    relay_pin.value(0)  # turn the relay off
    time.sleep(1)        # wait for 1 second
