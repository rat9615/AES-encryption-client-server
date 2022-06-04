import socket
from security.keys import generate_keys


def bind_connection():
    port = int(input("Enter the port you want the socket to bind to:\t"))
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((socket.gethostname(), port))
    server.listen(1)
    print(f"Listening to connections on port: {port}")
    return server


if __name__ == "__main__":
    generate_keys()
    server = bind_connection()

    while True:
        client, address = server.accept()
        print(f"\nEstablished connection request from client: {address}")
