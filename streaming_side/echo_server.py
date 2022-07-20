import socket
import random

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    conn.setblocking(0)
    with conn:
        print(f"Connected by {addr}")
        while True:
            # data = conn.recv(1024)
            # if not data:
            #     print("No Data")
            #     break
            data = "data "+str(random.randint(1,10))+" "
            conn.sendall(data.encode())