import socket
import threading

def handle_client(conn, addr):
    """Handle individual client connections"""
    
    try:
        while True:
            data = conn.recv(1024).decode('utf-8')
            
            if not data:
                break
            
            print(f"[{addr}] Received: {data}")
            
            echo_message = f"Echo: {data}"
            conn.send(echo_message.encode('utf-8'))
            
            if data.lower() == 'quit' or data.lower() == 'exit':
                print(f"[{addr}] Client requested to disconnect.")
                break
                
    except Exception as e:
        print(f"[ERROR] Error handling client {addr}: {e}")
    
    finally:
        conn.close()
        print(f"[DISCONNECTED] {addr} disconnected.")

def start_server(host="127.0.0.1", port=8080):
    """Start the echo server"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allow reuse of address
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((host, port))
        server.listen(5)
        print(f"[LISTENING] Echo server running on {host}:{port}")
        print(f"[INFO] Waiting for connections...")
        
        while True:
            conn, addr = server.accept()
            print(f"[NEW CONNECTION] {addr} connected.")
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.daemon = True  
            thread.start()
            
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
            
    except Exception as e:
        print(f"[ERROR] Server error: {e}")
    
    finally:
        server.close()

if __name__ == "__main__":
    start_server()

#python3 server.py
