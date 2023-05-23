import dht
from machine import Pin
import time

# create a DHT11 object
dht11 = dht.DHT11(Pin(2))

while True:
    try:
        # read the sensor data
        dht11.measure()
        temperature = dht11.temperature()
        humidity = dht11.humidity()

        # print the sensor data
        print("Temperature: %d C" % temperature)
        print("Humidity: %d %%" % humidity)

    except OSError as e:
        print("Failed to read sensor.")

    # wait for some time before taking another reading
    time.sleep(2)
