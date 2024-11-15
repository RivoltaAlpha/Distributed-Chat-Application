import socket
import threading

# Server configuration
SERVER_HOST = '127.0.0.1'
# you can also use the IP address of the machine you want to act like a server
SERVER_PORT = 12345
clients = []
usernames = {}  # Dictionary to keep track of clients and their usernames

# Broadcast message to all connected clients
def broadcast(message, client_socket):
    for client in clients:
       if client != client_socket:
            try:
                client.send(message)
            except:
                # Remove clients that are disconnected
                client.close()
                clients.remove(client)
                
                

# Handle individual client connections
def handle_client(client_socket):
     # Receive the username from the client
    try:
        username = client_socket.recv(1024).decode('utf-8')
        usernames[client_socket] = username
        print(f"{username} has joined the chat.")

        # Notify all clients about the new connection (except the new client)
        welcome_message = f"{username} has joined the chat."
        broadcast(welcome_message.encode('utf-8'), client_socket)

        while True:
            message = client_socket.recv(1024)
            if message:
                # Prepend the username to the message and broadcast it
                print(f"{username} says: {message.decode('utf-8')}")
                broadcast(f"{username}: {message.decode('utf-8')}".encode('utf-8'), client_socket)
            else:
                raise Exception("Client disconnected")
    except Exception as e:
        # Handle client disconnection
        print(f"{username} has left the chat.")
        # Notify all clients about the client leaving
        broadcast(f"{username} has left the chat.".encode('utf-8'), client_socket)
        
        # Clean up client data
        if client_socket in clients:
            clients.remove(client_socket)
        if client_socket in usernames:
            del usernames[client_socket]
        # close clients socket
        client_socket.close()
        
        
# Main server function with shutdown handling
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen()
    print("Server listening on", SERVER_HOST, ":", SERVER_PORT)

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"New connection from {client_address}")
            clients.append(client_socket)
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()
            # when server receives a keyboard interrupt
    except KeyboardInterrupt:
        print("\nServer is shutting down...")
        # Close all client connections
        for client in clients:
            client.close()
        server_socket.close()
        print("Server shutdown successfully.")

if __name__ == "__main__":
    start_server()
