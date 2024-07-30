import socket
import threading

# Configuración del cliente
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 54321

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

nickname = input("Elige tu nickname: ")

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == 'NICK':
                client_socket.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("Conexión cerrada")
            client_socket.close()
            break

threading.Thread(target=receive_messages).start()

while True:
    message = input()
    if message.lower() == 'salir':
        client_socket.send('salir'.encode('utf-8'))
        client_socket.close()
        break
    client_socket.send(message.encode('utf-8'))
