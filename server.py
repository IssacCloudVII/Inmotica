import network
import socket

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

# Receive data from the client and send a response
while True:
    data = conn.recv(1024)
    if not data:
        break
    num1, num2 = data.split(b",")
    print(num1)
    print(num2)
    result = int(num1) + int(num2)
    conn.send(str(result).encode())

# Clean up
conn.close()
s.close()
