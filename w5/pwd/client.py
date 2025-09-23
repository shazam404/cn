import socket

def run_client(host="127.0.0.1", port=9090):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    
    while True:
        password = input("Enter password (or 'exit'): ")
        if password.lower() == "exit":
            break
        client.send(password.encode())
        response = client.recv(1024).decode()
        print(f"Server: {response}")
    
    client.close()

if __name__ == "__main__":
    run_client()

#python3 server.py
#pythoon3 client.py
