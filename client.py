import socket
from utils import util
from time import sleep
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP as oaep


def create_connection():
    port = int(input("Enter the port you want the client to connect to:\t"))
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((socket.gethostname(), port))
    print(f"Connected to port: {port}")
    return server


def encrypt_password():
    with open("security/public_key.pem", "rb") as file_pub:
        key = RSA.import_key(file_pub.read())

    credentials = util.get_credentials()
    message = str.encode(credentials['app']['password'])
    encrypted_password = oaep.new(key).encrypt(message)
    return encrypted_password


def initialize_handshake():
    message = encrypt_password()
    server.send(message)
    print("\nInitiated handshake")


if __name__ == "__main__":
    server = create_connection()
    initialize_handshake()
    sleep(3)
