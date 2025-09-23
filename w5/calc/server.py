import socket
import threading

def handle_client(conn, addr):
    print("New connection from", addr)
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"Received from {addr}: {data.decode()}")
            
            try:
                decoded_data = data.decode().strip()
                op1, operator, op2 = decoded_data.split()
                op1, op2 = float(op1), float(op2)
                result = None
                print(f"Calculating: {op1} {operator} {op2}")
                if operator == '+':
                    result = op1 + op2
                elif operator == '-':
                    result = op1 - op2
                elif operator == '*':
                    result = op1 * op2
                elif operator == '/':
                    if op2 == 0:
                        result = "Error: Division by zero"
                    else:
                        result = op1 / op2
                else:
                    result = "Invalid operator"
                conn.send(str(result).encode())
            except Exception as e:
                conn.send(f"Error: {e}".encode())
    finally:
        conn.close()
        print(f"[DISCONNECTED] {addr} disconnected.")

def start_server(host="127.0.0.1", port=8080):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(2)  
    print(f"[LISTENING] Server running on {host}:{port}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()

# python3 server.py
