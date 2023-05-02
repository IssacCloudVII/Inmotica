import socket

host = '192.168.1.9'
port = 8000

# create socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the server
client_socket.connect((host, port))
print("Connected to server")

# send two numbers to the server
num1 = input("Tell me the number 1: ")
num2 = input("Tell me the number 2: ")
strSend = "{0},{1}".format(num1, num2)
client_socket.sendall(strSend.encode())

# receive the sum from the server
result = client_socket.recv(1024).decode()
print("The sum is: ", result)

# close the connection
client_socket.close()
