import socket
import threading

HOST = "localhost"
PORT = 8002

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((HOST, PORT))

sock.send(input("digite sua mensagem: ").encode())

confirmacao = sock.recv(1024)
if confirmacao == b"ok":
    print("mensagem recebida")