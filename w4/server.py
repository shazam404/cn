import socket
HOST = '127.0.0.1' # Localhost
PORT = 8080 # Port to listen on
# Create TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"Server listening on {HOST}:{PORT}...")
conn, addr = server_socket.accept()
print(f"Connected by {addr}")
# Receive message from client
data = conn.recv(1024).decode()
print(f"Client: {data}")
# Send response to client
response = "Hi Client, How are you?"
conn.sendall(response.encode())
# Close connections
conn.close()
server_socket.close()
