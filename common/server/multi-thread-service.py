import socket
import threading


def create_server_socket(host, port):
    s = socket.socket()
    s.bind((host, port))
    s.listen(5)
    print(f"server started on {host}:{port}")
    num = 0
    while True:
        num += 1
        conn, address = s.accept()
        print(f"server received from No.{num} connection, client {address}")
        client_handler = threading.Thread(target=handle_client, args=(conn, address, num))
        client_handler.start()


def handle_client(conn, address, num):
    while True:
        data: str = conn.recv(1024).decode('utf-8')
        print(f"client {num}:{address} send msg : {data}")
        msg = input(f"input you response to {num}:{address} msg:")
        if msg == 'exit' or msg == 'quit':
            break
        conn.send(msg.encode('utf-8'))
    conn.close()


if __name__ == '__main__':
    host = input(f"input host")
    port = int(input(f"input port"))
    create_server_socket(host, port)
