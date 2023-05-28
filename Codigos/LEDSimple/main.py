import machine
import time

led_pin = machine.Pin(2, machine.Pin.OUT)  # Replace with the appropriate GPIO pin number

while True:
    print("Prendiendo")
    led_pin.on()
    time.sleep(1)
    print("Apagando")
    led_pin.off()
    time.sleep(1)