import socket
import threading

# Para probar el login
username = input("Enter your username: ")

# Configuración del cliente
IP = "0.0.0.0"  # Conexión local
PORT = 5000
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

# Crear socket del cliente
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def receive_messages():
    while True:
        try:
            message = client.recv(SIZE).decode(FORMAT)

            if message == "@username":
                client.send(username.encode(FORMAT))
            else:
                print(message)
        except:
            print("Error al recibir el mensaje. Desconectando...")
            client.close()
            break

def write_messages():
    while True:
        message = input("")
        
        if message.upper() == "DESCONEXION":
            client.send(message.encode(FORMAT))
            print("Desconectando del servidor...")
            client.close()
            break
        
        client.send(f"{username}: {message}".encode(FORMAT))

# Crear hilos para recibir y escribir mensajes
receive_thread = threading.Thread(target=receive_messages, daemon=True)
receive_thread.start()

write_thread = threading.Thread(target=write_messages, daemon=True)
write_thread.start()

# Esperar a que el usuario cierre el programa
write_thread.join()
