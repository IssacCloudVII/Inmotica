import machine
import time

led_pin = machine.Pin(2, machine.Pin.OUT)  # Replace with the appropriate GPIO pin number

while True:
    led_pin.on()
    time.sleep(5)
    led_pin.off()
    time.sleep(5)