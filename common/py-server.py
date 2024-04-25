import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", 8888))
s.listen(5)
print(f"server listening on port 8888,waiting for client connection")
while True:
    conn, address = s.accept()
    print(f"received connection from: {address}")
    while True:
        data: str = conn.recv(1024).decode("UTF-8")
        print(f"received data: {data}")
        msg = input("Enter your message: ")
        if msg == 'exit' or msg == 'quit':
            break
        conn.send(msg.encode("UTF-8"))

    conn.close()
    s.close()
