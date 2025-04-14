import socket
import threading
import os

class ChatClient:

    def __init__(self, host, port=12345, username='User'):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        self.username = username
        self.chat_log_file = f"{username}_chat_history.txt"

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                print(message)
                self.save_to_history(message)
            except:
                print("Disconnected from server.")
                break

    def send_messages(self):
        while True:
            message = input()
            full_message = f"{self.username}: {message}"
            self.client_socket.sendall(full_message.encode())
            self.save_to_history(full_message)

    def save_to_history(self, message):
        with open(self.chat_log_file, "a", encoding="utf-8") as file:
            file.write(message + "\n")

    def start(self):
        threading.Thread(target=self.receive_messages, daemon=True).start()
        self.send_messages()

if __name__ == "__main__":
    name = input("Enter your username: ")
    client = ChatClient(host='172.16.153.149', username=name)
    client.start()
