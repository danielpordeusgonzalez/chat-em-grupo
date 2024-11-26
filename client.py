import socket
import threading

# Função para receber mensagens do servidor
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Conexão encerrada pelo servidor.")
            client_socket.close()
            break

server_ip = "localhost" 
server_port = 8002

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

thread = threading.Thread(target=receive_messages, args=(client_socket,))
thread.start()

while True:
    message = input()
    client_socket.send(message.encode('utf-8'))
    if message.lower() == 'sair':
        print("Você saiu do chat.")
        break

client_socket.close()

