import socket
import threading

# Server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

# Function to receive messages from server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Connection closed by server.")
            client_socket.close()
            break

# Main client function
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    
    # Start receiving thread
    thread = threading.Thread(target=receive_messages, args=(client_socket,))
    thread.start()

    while True:
        message = input()
        if message.lower() == 'exit':
            client_socket.close()
            break
        client_socket.send(message.encode('utf-8'))

if __name__ == "__main__":
    start_client()
