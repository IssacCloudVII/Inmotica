from machine import Pin, PWM, ADC
import time
import dht

def changeColor(red, green, blue):
    red_pwm.duty(red)
    green_pwm.duty(green)
    blue_pwm.duty(blue)

def read_temperature(pins):
    temperatures = []
    for pin in pins:
        temp = pin.read()
        temperatures.append(temp)
    return temperatures

# Pines de termopar
termoparActive = Pin(18, Pin.OUT)
bombaPin1 = Pin(15, Pin.OUT)  # Bomba caliente
bombaPin2 = Pin(2, Pin.OUT)  # Bomba fría
placaPeltierPin1 = Pin(4, Pin.OUT)  # Peltier caliente
placaPeltierPin2 = Pin(16, Pin.OUT)  # Peltier fría
ventiladorPin = Pin(5, Pin.OUT)

# Pines de detección
buzzerPin = Pin(3, Pin.OUT)  # Detector de llama
flamePin = ADC(Pin(12))  # Pin ADC para detección de llama
smokeLED = Pin(21, Pin.OUT)  # LED de detección de humo
smokePin = ADC(Pin(13))  # Pin ADC para detección de humo

# Pines para el LED RGB
red_pin = Pin(1, Pin.OUT)
green_pin = Pin(22, Pin.OUT)
blue_pin = Pin(23, Pin.OUT)

# Pines de termopar
termopar_pins = [
    ADC(Pin(14)),  # Serpentin frio
    ADC(Pin(27)),  # Serpentin caliente
    ADC(Pin(25)),  # Peltier caliente
    ADC(Pin(26)),  # Peltier fria
    ADC(Pin(33)),  # Entrada
    ADC(Pin(32)),  # Salida
]

# Sensor DHT11
sensor = dht.DHT11(Pin(19))

# set up PWM objects for each pin
red_pwm = PWM(red_pin, freq=1000)
green_pwm = PWM(green_pin, freq=1000)
blue_pwm = PWM(blue_pin, freq=1000)

# set initial RGB values
red_value = 0
green_value = 0
blue_value = 0

# set the RGB values to turn on the LED to white
# red_value = 255
# green_value = 255
# blue_value = 255

# set the duty cycles for each pin
red_pwm.duty(red_value)
green_pwm.duty(green_value)
blue_pwm.duty(blue_value)
changeColor(0, 0, 255)

verde = False
blanco = True
apagado = False

while True:
    termoparActive.on()
    temperatures = read_temperature(termopar_pins)
    temperatureAverage = sum(temperatures) / len(temperatures)
    # read the analog voltage from the ADC pin
    flameVoltage = flamePin.read() / 1023 * 2.727
    if flameVoltage < 1.8:
        changeColor(255, 0, 0)
        buzzerPin.on()
    else:
        changeColor(0, 0, 255)
        buzzerPin.off()

    valuePPM = smokePin.read()
    if valuePPM > 1200:
        changeColor(255, 0, 255)
        smokeLED.on()
    else:
        changeColor(0, 0, 255)
        smokeLED.off()
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    temp_f = temp * (9/5) + 32.0

    if blanco:
        changeColor(255, 255, 255)
        bombaPin1.on()
        bombaPin2.on()

    if verde:
        bombaPin1.off()
        bombaPin2.off()
        placaPeltierPin1.on()
        placaPeltierPin2.on()
        ventiladorPin.on()

    if apagado:
        changeColor(0, 0, 0)
        bombaPin1.off()
        bombaPin2.off()
        placaPeltierPin1.off()
        placaPeltierPin2.off()
        ventiladorPin.off()

    print('Temperature: %3.1f C' %temp)
    print('Temperature: %3.1f F' %temp_f)
    print('Humidity: %3.1f %%' %hum)
    print("Ciclo terminado")
    time.sleep(1)