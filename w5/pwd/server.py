import socket
import threading
import re

def validate_password(password):
    if not (8 <= len(password) <= 20):
        return "Invalid: Length must be between 8 and 20"
    if not re.search(r"[a-z]", password):
        return "Invalid: Must contain a lowercase letter"
    if not re.search(r"[A-Z]", password):
        return "Invalid: Must contain an uppercase letter"
    if not re.search(r"[0-9]", password):
        return "Invalid: Must contain a digit"
    if not re.search(r"[_@$]", password):
        return "Invalid: Must contain at least one special char (_,@,$)"
    return "Valid Password"

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            response = validate_password(data)
            conn.send(response.encode())
    finally:
        conn.close()
        print(f"[DISCONNECTED] {addr} disconnected.")

def start_server(host="127.0.0.1", port=9090):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[LISTENING] Password server running on {host}:{port}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
