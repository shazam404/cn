import socket
import threading
import sys

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if not msg:
                break
            print(msg)
        except:
            break

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python client.py A|B username")
        sys.exit(0)

    server_choice = sys.argv[1].upper()
    username = sys.argv[2]
    host = "127.0.0.1"

    if server_choice == "A":
        port = 9000
    elif server_choice == "B":
        port = 9010
    else:
        print("Invalid choice! Use A or B")
        sys.exit(0)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print(f"[CONNECTED] to Server {server_choice} as {username}")

    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

    while True:
        msg = input()
        if msg.lower() == "exit":
            break
        full_msg = f"{username}: {msg}"
        sock.sendall(full_msg.encode())

    sock.close()
