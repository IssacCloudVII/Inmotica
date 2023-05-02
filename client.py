import socket

host = '192.168.1.9'
port = 8000

# create socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the server
client_socket.connect((host, port))
print("Connected to server")

# send two numbers to the server
client_socket.sendall("10,20".encode())

# receive the sum from the server
result = client_socket.recv(1024).decode()
print("The sum is: ", result)

# close the connection
client_socket.close()
