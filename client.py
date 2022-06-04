import socket


def create_connection():
    port = int(input("Enter the port you want the client to connect to:\t"))
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((socket.gethostname(), port))
    print(f"Connected to port: {port}")
    return server


if __name__ == "__main__":
    server = create_connection()
