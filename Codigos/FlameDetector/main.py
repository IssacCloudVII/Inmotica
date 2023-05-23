from machine import Pin, ADC
import time

# set up the flame detector pin
buzzerPin = Pin(4, Pin.OUT)
# set up the ADC pin
adc = ADC(Pin(2))

while True:
    # read the analog voltage from the ADC pin
    voltage = adc.read() / 1023 * 2.727

    if voltage < 1.8:
        print("Hay flama perres. " + str(voltage) + " V")
        buzzerPin.on()
    else:
        print("No flama perres :c. " + str(voltage) + " V")
        buzzerPin.off()

    if valuePPM > 1200:
        print("GAS GAS GAS")
        led_pin.on()
    else:
        print("NADA NADA NADA")
        led_pin.off()

    # wait for some time before taking another reading
    time.sleep(0.1)

#Nivelar la luz porque el sensor detecta la luz y el voltaje sube demasiado si hay mucha luz y detecta flama cuando no.