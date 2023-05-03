import socket
import time

host = '192.168.1.9'
port = 8000

# create socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the server
client_socket.connect((host, port))
print("Connected to server")

try:
    # receive and print temperatures indefinitely
    while True:
        # unpack the temperature data using struct
        temperature_string = client_socket.recv(1024).decode()
        temperatures = [float(temp) for temp in temperature_string.split(",")]

        # print the temperatures
        print("Received temperatures:", temperatures)

        # wait for a few seconds before receiving again
        time.sleep(2)

except KeyboardInterrupt:
    # close the connection and exit the program when Ctrl+C is pressed
    client_socket.close()
    print("\nProgram terminated by user.")