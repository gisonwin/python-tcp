import socket

socket_client = socket.socket()
socket_client.connect(('127.0.0.1', 8888))
while True:
    send_msg = input("input message send to server:")
    if send_msg == 'quit' or send_msg == 'exit':
        break
    socket_client.send(send_msg.encode("UTF-8"))
    recv_data = socket_client.recv(2014).decode("UTF-8")
    print(f"Received from server msg: {recv_data}")
socket_client.close()
