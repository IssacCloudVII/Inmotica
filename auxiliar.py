from machine import Pin, PWM, ADC
import network
import socket
import random
import time

def generateTemperature():
    minTemp = 20
    maxTemp = 40
    diff = maxTemp - minTemp
    temperatures = []
    
    for i in range(0, 8):
        temperature = minTemp + random.random() * diff
        temperatures.append(temperature)

    return temperatures

def read_temperature(pins):

    return generateTemperature()

    temperatures = []
    for pin in pins:
        temp = pin.read()
        temperatures.append(temp)
    return temperatures


# Set up the WiFi connection
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect("SpongeBob Extreme", "7734bbd7d3fea0dc77f77600e9")

# Wait until the connection is established
while not sta_if.isconnected():
    pass

# Set up the socket server
s = socket.socket()
s.bind(('', 8000))
s.listen(1)

# Wait for a client to connect
print('IP address:', sta_if.ifconfig()[0])
print("Waiting for a client to connect...")
conn, addr = s.accept()
print("Connected by", addr)
time.sleep(3)

while True:
    temperatures = generateTemperature()
    print("Enviando")
    temperature_string = ",".join(str(temp) for temp in temperatures)
    conn.sendall(temperature_string.encode())
    time.sleep(1)

# Pines de termopar
termoparActive = Pin(18, Pin.OUT)
bombaPin1 = Pin(15, Pin.OUT)  # Bomba caliente
bombaPin2 = Pin(2, Pin.OUT)  # Bomba fr�a
placaPeltierPin1 = Pin(4, Pin.OUT)  # Peltier caliente
placaPeltierPin2 = Pin(16, Pin.OUT)  # Peltier fr�a
ventiladorPin = Pin(5, Pin.OUT)

# Pines de detecci�n
buzzerPin = Pin(3, Pin.OUT)  # Detector de llama
flamePin = ADC(Pin(12))  # Pin ADC para detecci�n de llama
smokeLED = Pin(21, Pin.OUT)  # LED de detecci�n de humo
smokePin = ADC(Pin(13))  # Pin ADC para detecci�n de humo

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
    temperatures = read_temperature(termopar_pins)
    temperatureAverage = sum(temperatures) / len(temperatures)

    temperature_string = ",".join(str(temp) for temp in temperatures)
    conn.sendall(temperature_string.encode())

    continue
    termoparActive.on()

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

    ventiladorPin.off()
    
    placaPeltierPin1.off()

    placaPeltierPin2.off()

    bombaPin1.off()

    bombaPin2.off()

    changeColor(0, 0, 0)
