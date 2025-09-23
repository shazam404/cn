import socket

HOST = '127.0.0.1'  # Server IP (localhost)
PORT = 8080  # Same port as server

# Create TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Send message to server
message = "Hello Server"
client_socket.sendall(message.encode())
print("Message sent to server")

# Receive response from server
data = client_socket.recv(1024).decode()
print(f"Server: {data}")

# Close connection
client_socket.close()
