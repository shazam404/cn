import socket

def run_client(host="127.0.0.1", port=8080):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print(f"Connected to server at {host}:{port}")
    
    while True:
        expr = input("Enter expression (e.g., 3 + 4) or 'exit' to quit: ")
        if expr.lower() == 'exit':
            break
        client.send(expr.encode())
        response = client.recv(1024).decode()
        print("Result from server:", response)

    client.close()
    print("Disconnected from server.")

if __name__ == "__main__":
    run_client()

# python3 client.py
