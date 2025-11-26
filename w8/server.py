import threading
import socket
import sys

clients = []
lock = threading.Lock()
udp_sock = None

def broadcast(msg):
    with lock:
        for c, p in clients[:]:
            try:
                if p == 'tcp':
                    c.send(msg.encode())
                else:
                    udp_sock.sendto(msg.encode(), c)
            except:
                clients.remove((c, p))

def forward_to_other(other_port, msg):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', other_port))
        s.send(("FWD:" + msg).encode())
        s.close()
    except:
        pass

def handle_tcp(conn, other_port):
    try:
        msg = conn.recv(1024).decode()
    except:
        return
    if not msg:
        return
    
    if msg.startswith("FWD:"):
        fwd_msg = msg[4:]
        print("Forwarded:", fwd_msg)
        broadcast(fwd_msg)
        conn.close()
        return
    
    with lock:
        clients.append((conn, 'tcp'))
    
    broadcast(msg)
    print("TCP Client:", msg)
    forward_to_other(other_port, msg)
    
    while True:
        try:
            data = conn.recv(1024).decode()
        except:
            break
        if not data:
            break
        broadcast(data)
        print("TCP Client:", data)
        forward_to_other(other_port, data)
    
    with lock:
        if (conn, 'tcp') in clients:
            clients.remove((conn, 'tcp'))
    try:
        conn.close()
    except:
        pass

def handle_udp(sock, other_port):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            msg = data.decode()
        except:
            break
        
        found = False
        with lock:
            for c, p in clients:
                if p == 'udp' and c == addr:
                    found = True
                    break
            if not found:
                clients.append((addr, 'udp'))
        
        broadcast(msg)
        print("UDP Client:", msg)
        forward_to_other(other_port, msg)

num = sys.argv[1]
if num == "1":
    my_port = 6001
    other_port = 6002
else:
    my_port = 6002
    other_port = 6001

tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp_sock.bind(('127.0.0.1', my_port))
tcp_sock.listen(10)

udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_sock.bind(('127.0.0.1', my_port + 100))

print(f"Server {num} running on TCP:{my_port}, UDP:{my_port + 100}")

threading.Thread(target=handle_udp, args=(udp_sock, other_port), daemon=True).start()

try:
    while True:
        conn, addr = tcp_sock.accept()
        threading.Thread(target=handle_tcp, args=(conn, other_port), daemon=True).start()
except:
    tcp_sock.close()
    udp_sock.close()
