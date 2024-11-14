import socket
import threading
from plyer import notification
from playsound import playsound
import winsound


# Server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

# Function to receive messages from server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
                winsound.PlaySound('./notification_sound.wav', winsound.SND_FILENAME)
                notification.notify(
                    title="New Message",
                    message=message,
                    timeout=5  # Notification will disappear after 5 seconds
                )
            else:
                print("Server closed the connection.")
                client_socket.close()
                break
        except:
            print("Disconnected from server.")
            client_socket.close()
            break

# Main client function
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
    except ConnectionRefusedError:
        print("Server is unavailable. Exiting.")
        return
    # Get a username from the user
    username = input("Enter your username: ")
    client_socket.send(username.encode('utf-8'))
    # Start receiving thread
    thread = threading.Thread(target=receive_messages, args=(client_socket,))
    thread.start()

    try:
        while True:
            message = input()
            if message.lower() == 'exit':
                client_socket.close()
                print("You have exited the chat.")
                break
            client_socket.send(message.encode('utf-8'))
    except KeyboardInterrupt:
        print("\nExiting chat...")
        client_socket.close()

if __name__ == "__main__":
    start_client()
