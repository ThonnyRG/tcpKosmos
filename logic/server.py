import socket
import threading

# Configuración del servidor
IP = "0.0.0.0"
PORT = 5000
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

# Crear y configurar el servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()

print(f"Servidor en ejecución en {ADDR}")

# Lista para almacenar clientes activos
clients = []
usernames = []

def broadcast(message, sender_client):
    for client in clients:
        if client != sender_client:
            try:
                client.send(message)
            except:
                remove_client(client)

def remove_client(client):
    if client in clients:
        index = clients.index(client)
        username = usernames[index]
        print(f"{username} se ha desconectado.")
        broadcast(f"{username} ha salido del chat.".encode(FORMAT), client)
        clients.remove(client)
        usernames.pop(index)
        client.close()

def handle_messages(client):
    while True:
        try:
            message = client.recv(SIZE)
            if message.decode(FORMAT).upper() == "DESCONEXION":
                remove_client(client)
                break
            broadcast(message, client)
        except:
            remove_client(client)
            break

def receive_connections():
    while True:
        client, address = server.accept()

        # Solicitar y recibir el nombre de usuario
        client.send("@username".encode(FORMAT))
        username = client.recv(SIZE).decode(FORMAT)

        # Agregar cliente y usuario a las listas
        clients.append(client)
        usernames.append(username)

        print(f"{username} conectado desde {str(address)}")

        # Notificar a los demás usuarios
        welcome_message = f"{username} se ha unido al chat.".encode(FORMAT)
        broadcast(welcome_message, client)

        # Confirmar conexión al cliente
        client.send("Conectado al servidor".encode(FORMAT))

        # Iniciar un hilo para manejar los mensajes del cliente
        thread = threading.Thread(target=handle_messages, args=(client,))
        thread.start()

# Iniciar el servidor
receive_connections()
