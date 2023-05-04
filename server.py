from machine import Pin
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

# Generate and send temperatures to the client
while True: 
    temperatures = generateTemperature()
    print(temperatures)
    temperature_string = ",".join(str(temp) for temp in temperatures)
    conn.sendall(temperature_string.encode())
    time.sleep(2)

# Clean up
conn.close()
s.close()
