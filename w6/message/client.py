import socket

def run_client(host="127.0.0.1", port=8080):
    """Run the echo client"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((host, port))
        print(f"[CONNECTED] Connected to echo server at {host}:{port}")
        print("[INFO] Type 'quit' or 'exit' to disconnect from server")
        print("-" * 50)
        
        while True:
            message = input("Enter message: ")
            
            if not message.strip():
                print("[WARNING] Please enter a non-empty message")
                continue
            
            client.send(message.encode('utf-8'))
            response = client.recv(1024).decode('utf-8')
            
            print(f"Server response: {response}")
            
            if message.lower() == 'quit' or message.lower() == 'exit':
                print("[INFO] Disconnecting from server...")
                break
                
    except ConnectionRefusedError:
        print("[ERROR] Could not connect to server. Make sure the server is running.")
    except Exception as e:
        print(f"[ERROR] Client error: {e}")
    
    finally:
        client.close()
        print("[DISCONNECTED] Client disconnected.")

if __name__ == "__main__":
    run_client()

#python3 client.py
