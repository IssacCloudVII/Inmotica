from machine import Pin, ADC
import time

# set up the smoke detector pin
led_pin = Pin(33, Pin.OUT)

# set up the ADC pin
adc = ADC(Pin(2))

while True:
    # read the analog voltage from the ADC pin
    valuePPM = adc.read()

    if valuePPM > 1200:
        print("GAS GAS GAS")
        led_pin.on()
    else:
        print("NADA NADA NADA")
        led_pin.off()

    print("PPM: %.2f u" % valuePPM)

    # wait for some time before taking another reading
    time.sleep(0.3)
