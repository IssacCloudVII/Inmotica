from machine import Pin, ADC
import time

# set up the ADC pin
adc = ADC(Pin(2))

while True:
    # read the analog voltage from the ADC pin
    temp = adc.read()

    print("Temperatura: " + str(temp))

    # wait for some time before taking another reading
    time.sleep(0.5)
