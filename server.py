import socket
import threading

rooms = {}

def handle_client(client_socket, client_address):
    try:

        client_socket.send("Digite seu nome: ".encode('utf-8'))
        name = client_socket.recv(1024).decode('utf-8')

        client_socket.send("Digite o nome da sala: ".encode('utf-8'))
        room = client_socket.recv(1024).decode('utf-8')

        if room not in rooms:
            rooms[room] = []
        rooms[room].append((client_socket, name))

        broadcast(f"{name} entrou na sala {room}.", room, client_socket)

        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if message.lower() == 'sair':
                break
            broadcast(f"{name}: {message}", room, client_socket)

    except Exception as e:
        print(f"Erro com {client_address}: {e}")

    finally:
        if room in rooms:
            rooms[room] = [(sock, n) for sock, n in rooms[room] if sock != client_socket]
            broadcast(f"{name} saiu da sala {room}.", room, client_socket)

        client_socket.close()


def broadcast(message, room, sender_socket):
    if room in rooms:
        for client_socket, _ in rooms[room]:
            if client_socket != sender_socket:
                try:
                    client_socket.send(message.encode('utf-8'))
                except:
                    client_socket.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 8002))
server.listen(5)

print("Servidor rodando...")

while True:
    client_socket, client_address = server.accept()
    print(f"Nova conexão de {client_address}")
    threading.Thread(target=handle_client, args=(client_socket, client_address)).start()