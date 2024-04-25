import socket


def create_client(host, port):
    sc = socket.socket()
    sc.connect((host, port))
    while True:
        msg = input(f"input msg send to server:{host}:{port} msg :")
        if msg == 'exit' or msg == 'quit':
            break
        sc.send(msg.encode("utf-8"))
        server_data = sc.recv(1024).decode("utf-8")
        print(f"client received server msg : {server_data}")
    sc.close()


if __name__ == '__main__':
    client_host = input(f"input host")
    client_port = int(input(f"input port"))
    create_client(client_host, client_port)
