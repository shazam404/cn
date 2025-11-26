import threading
import socket

def recv_tcp(s):
    while True:
        try:
            data = s.recv(1024).decode()
        except:
            break
        if not data:
            break
        print("\n" + data)

def recv_udp(s):
    while True:
        try:
            data, addr = s.recvfrom(1024)
            print("\n" + data.decode())
        except:
            break

proto = input("Protocol (tcp/udp): ").lower()
server = input("Server (1/2): ")
name = input("Your name: ")

if server == "1":
    tcp_port = 6001
    udp_port = 6101
else:
    tcp_port = 6002
    udp_port = 6102

if proto == 'tcp':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', tcp_port))
    print(f"Connected to Server {server} via TCP")
    
    s.send((name + " joined").encode())
    threading.Thread(target=recv_tcp, args=(s,), daemon=True).start()
    
    while True:
        msg = input()
        if not msg:
            continue
        if msg.lower() == "exit":
            break
        try:
            s.send((name + ": " + msg).encode())
        except:
            break
    
    try:
        s.close()
    except:
        pass

else:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"Connected to Server {server} via UDP")
    
    s.sendto((name + " joined").encode(), ('127.0.0.1', udp_port))
    threading.Thread(target=recv_udp, args=(s,), daemon=True).start()
    
    while True:
        msg = input()
        if not msg:
            continue
        if msg.lower() == "exit":
            break
        try:
            s.sendto((name + ": " + msg).encode(), ('127.0.0.1', udp_port))
        except:
            break
    
    try:
        s.close()
    except:
        pass
