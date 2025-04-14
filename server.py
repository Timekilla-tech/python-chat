import socket
import threading

class ChatServer:
    def __init__(self, host='Ip address', port=12345):
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        print(f"Server running on {host}:{port}")

    def broadcast(self, message, sender_socket):
        for client in self.clients:
            if client != sender_socket:
                client.sendall(message)

    def handle_client(self, client_socket, address):
        print(f"New connection from {address}")
        while True:
            try:
                message = client_socket.recv(1024)
                if not message:
                    break
                self.broadcast(message, client_socket)
            except:
                break
        client_socket.close()
        self.clients.remove(client_socket)
        print(f"{address} disconnected.")

    def run(self):
        while True:
            client_socket, address = self.server_socket.accept()
            self.clients.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket, address)).start()

if __name__ == "__main__":
    server = ChatServer()
    server.run()