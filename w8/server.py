import socket
import threading
import sys

tcp_clients = []
udp_clients = []  
peer_conn = None  
server_role = None
udp_socket_global = None  

clients_lock = threading.Lock()

def broadcast_tcp(message, source_conn=None):
    with clients_lock:
        for client in tcp_clients[:]:
            try:
                if client != source_conn:
                    client.sendall(message.encode())
            except:
                tcp_clients.remove(client)

def broadcast_udp(message, source_addr=None):
    global udp_socket_global
    if not udp_socket_global:
        return
    with clients_lock:
        for addr in udp_clients[:]:
            try:
                if addr != source_addr:
                    udp_socket_global.sendto(message.encode(), addr)
            except:
                udp_clients.remove(addr)

def broadcast_all(message, source_conn=None, source_addr=None):
    broadcast_tcp(message, source_conn)
    broadcast_udp(message, source_addr)

def handle_tcp_client(conn, addr):
    print(f"[TCP CLIENT] {addr} connected")
    try:
        while True:
            msg = conn.recv(1024).decode()
            if not msg:
                break
            print(f"[TCP {addr}] {msg}")

            broadcast_all(msg, source_conn=conn)

            if peer_conn:
                try:
                    peer_conn.sendall(f"[FORWARD]{msg}".encode())
                except:
                    pass
    except Exception as e:
        print(f"[TCP ERROR] {addr}: {e}")
    finally:
        conn.close()
        with clients_lock:
            if conn in tcp_clients:
                tcp_clients.remove(conn)
        print(f"[TCP DISCONNECTED] {addr}")

def tcp_client_listener(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    
    while True:
        conn, addr = server.accept()
        with clients_lock:
            tcp_clients.append(conn)
        threading.Thread(target=handle_tcp_client, args=(conn, addr), daemon=True).start()

def udp_client_listener(host, port):
    global udp_socket_global
    udp_socket_global = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket_global.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_socket_global.bind((host, port))
    
    while True:
        try:
            data, addr = udp_socket_global.recvfrom(1024)
            msg = data.decode()
            
            if msg.startswith("[REGISTER]"):
                with clients_lock:
                    if addr not in udp_clients:
                        udp_clients.append(addr)
                        print(f"[UDP CLIENT] {addr} registered")
                udp_socket_global.sendto("[REGISTERED]".encode(), addr)
                continue
            
            if msg.startswith("[DISCONNECT]"):
                with clients_lock:
                    if addr in udp_clients:
                        udp_clients.remove(addr)
                        print(f"[UDP DISCONNECTED] {addr}")
                continue
            
            print(f"[UDP {addr}] {msg}")
            
            broadcast_all(msg, source_addr=addr)
            
            if peer_conn:
                try:
                    peer_conn.sendall(f"[FORWARD]{msg}".encode())
                except:
                    pass
                    
        except Exception as e:
            print(f"[UDP ERROR] {e}")

def peer_listener(host, port):
    global peer_conn
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(1)
    
    peer_conn, addr = server.accept()
    print(f"[PEER CONNECTED] Server B connected from {addr}")
    handle_peer(peer_conn)

def connect_to_peer(host, port):
    global peer_conn
    peer_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    while True:
        try:
            peer_conn.connect((host, port))
            print(f"[PEER CONNECTED] Connected to Server A at {host}:{port}")
            break
        except:
            continue
    
    handle_peer(peer_conn)

def handle_peer(conn):
    while True:
        try:
            msg = conn.recv(1024).decode()
            if not msg:
                break
            
            if msg.startswith("[FORWARD]"):
                actual_msg = msg[9:] 
                print(f"[PEER MSG] {actual_msg}")
                broadcast_all(actual_msg)
        except Exception as e:
            print(f"[PEER ERROR] {e}")
            break

def start_server(role):
    global server_role
    server_role = role
    host = "127.0.0.1"
    
    if role == "A":
        client_tcp_port = 9000
        client_udp_port = 9002
        peer_port = 9001
        
        print(f"\n{'='*50}")
        print(f"  SERVER A - Distributed Chatroom")
        print(f"{'='*50}\n")
        
        tcp_thread = threading.Thread(target=tcp_client_listener, args=(host, client_tcp_port), daemon=True)
        tcp_thread.start()
        
        udp_thread = threading.Thread(target=udp_client_listener, args=(host, client_udp_port), daemon=True)
        udp_thread.start()
        
        peer_listener(host, peer_port)
        
    elif role == "B":
        client_tcp_port = 9010
        client_udp_port = 9012
        peer_host = host
        peer_port = 9001
        
        print(f"\n{'='*50}")
        print(f"  SERVER B - Distributed Chatroom")
        print(f"{'='*50}\n")
        
        tcp_thread = threading.Thread(target=tcp_client_listener, args=(host, client_tcp_port), daemon=True)
        tcp_thread.start()
        
        udp_thread = threading.Thread(target=udp_client_listener, args=(host, client_udp_port), daemon=True)
        udp_thread.start()
        
        connect_to_peer(peer_host, peer_port)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python server.py A|B")
        print("  A - Start as Server A (primary)")
        print("  B - Start as Server B (secondary)")
        sys.exit(1)
    
    role = sys.argv[1].upper()
    if role not in ["A", "B"]:
        print("Invalid role! Use A or B.")
        sys.exit(1)
    
    start_server(role)
