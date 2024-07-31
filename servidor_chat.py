import socket
import threading

#Configuración del servidor
host = '127.0.0.1'
port = 54321

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

print(f"Servidor On y no fire {host}:{port}")

clientes = []
usernames = {}

def broadcast(message, exclude_client):
    for cliente in clientes:
        if cliente != exclude_client:
            try:
                cliente.send(message)
            except:
                # Si el envío falla, cerrar el cliente y eliminarlo
                cliente.close()
                if cliente in clientes:
                    clientes.remove(cliente)

def handle_client(cliente):
    while True:
        try:
            message = cliente.recv(1024)
            if not message:
                raise ConnectionResetError("Cliente desconectado")
            if message.decode('utf-8').lower() == 'chau':
                raise ConnectionResetError("Cliente desconectado")
            print(f"Mensaje recibido de {usernames[cliente]}: {message.decode('utf-8')}")
            broadcast(f"{usernames[cliente]}: {message.decode('utf-8')}".encode('utf-8'), cliente)
        except (ConnectionResetError, ConnectionAbortedError):
            if cliente in clientes:
                clientes.remove(cliente)
            broadcast(f"{usernames[cliente]} se ha desconectado".encode('utf-8'), cliente)
            del usernames[cliente]
            cliente.close()
            break

def receive_connections():
    while True:
        try:
            cliente, address = server.accept()
            cliente.send("NICK".encode('utf-8'))
            nickname = cliente.recv(1024).decode('utf-8')
            clientes.append(cliente)
            usernames[cliente] = nickname
            print(f"{nickname} está conectado con {str(address)}")
            broadcast(f"{nickname} se ha unido al chat".encode('utf-8'), cliente)
            cliente.send("Conectado al chatsito. Escribi 'chau' para desconectarte.".encode('utf-8'))
            threading.Thread(target=handle_client, args=(cliente,)).start()
        except KeyboardInterrupt:
            print("Servidor apagado.")
            for cliente in clientes:
                cliente.close()
            server.close()
            break

receive_connections()
