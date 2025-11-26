import socket
import threading
import sys

def receive_tcp_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if not msg:
                break
            print(f"\n{msg}")
            print("You: ", end="", flush=True)
        except:
            break
    print("\n[DISCONNECTED] Connection to server lost.")

def receive_udp_messages(sock):
    while True:
        try:
            data, _ = sock.recvfrom(1024)
            msg = data.decode()
            if msg == "[REGISTERED]":
                continue
            print(f"\n{msg}")
            print("You: ", end="", flush=True)
        except:
            break

def run_tcp_client(host, port, username):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        sock.connect((host, port))
        print(f"[CONNECTED] Connected to server via TCP at {host}:{port}")
        print(f"[INFO] Logged in as: {username}")
        print("[INFO] Type 'exit' to quit\n")
        
        threading.Thread(target=receive_tcp_messages, args=(sock,), daemon=True).start()
        
        while True:
            msg = input("You: ")
            if msg.lower() == "exit":
                break
            if msg.strip():
                full_msg = f"[TCP] {username}: {msg}"
                sock.sendall(full_msg.encode())
                
    except ConnectionRefusedError:
        print("[ERROR] Could not connect to server. Make sure server is running.")
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        sock.close()
        print("[DISCONNECTED] Goodbye!")

def run_udp_client(host, port, username):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_addr = (host, port)
    
    try:
        sock.sendto("[REGISTER]".encode(), server_addr)
        
        sock.settimeout(5)
        try:
            data, _ = sock.recvfrom(1024)
            if data.decode() == "[REGISTERED]":
                print(f"[CONNECTED] Connected to server via UDP at {host}:{port}")
                print(f"[INFO] Logged in as: {username}")
                print("[INFO] Type 'exit' to quit")
                print("[NOTE] UDP mode - messages may be lost or arrive out of order\n")
        except socket.timeout:
            print("[ERROR] Server did not respond. Make sure server is running.")
            return
        
        sock.settimeout(None)
        
        threading.Thread(target=receive_udp_messages, args=(sock,), daemon=True).start()
        
        while True:
            msg = input("You: ")
            if msg.lower() == "exit":
                sock.sendto("[DISCONNECT]".encode(), server_addr)
                break
            if msg.strip():
                full_msg = f"[UDP] {username}: {msg}"
                sock.sendto(full_msg.encode(), server_addr)
                
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        sock.close()
        print("[DISCONNECTED] Goodbye!")

def main():
    print("\n" + "=" * 50)
    print("  DISTRIBUTED CHATROOM CLIENT")
    print("=" * 50)
    
    if len(sys.argv) < 4:
        print("\nUsage: python client.py <A|B> <TCP|UDP> <username>")
        print("\nExamples:")
        print("  python client.py A TCP Alice    # Connect to Server A via TCP")
        print("  python client.py B UDP Bob      # Connect to Server B via UDP")
        print("\nServer Details:")
        print("  Server A: TCP=9000, UDP=9002")
        print("  Server B: TCP=9010, UDP=9012")
        sys.exit(1)
    
    server_choice = sys.argv[1].upper()
    protocol = sys.argv[2].upper()
    username = sys.argv[3]
    
    host = "127.0.0.1"
    
    if server_choice == "A":
        tcp_port = 9000
        udp_port = 9002
    elif server_choice == "B":
        tcp_port = 9010
        udp_port = 9012
    else:
        print("[ERROR] Invalid server choice! Use A or B.")
        sys.exit(1)
    
    print(f"\n  Server: {server_choice}")
    print(f"  Protocol: {protocol}")
    print(f"  Username: {username}")
    print("=" * 50 + "\n")
    
    if protocol == "TCP":
        run_tcp_client(host, tcp_port, username)
    elif protocol == "UDP":
        run_udp_client(host, udp_port, username)
    else:
        print("[ERROR] Invalid protocol! Use TCP or UDP.")
        sys.exit(1)

if __name__ == "__main__":
    main()

# python3 server.py A
# python3 server.py B
# python3 client.py A TCP Alice
# python3 client.py A UDP Bob
# python3 client.py B UDP Charlie
# python3 client.py B TCP Dave
