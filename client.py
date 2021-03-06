import socket
from utils import util
from time import sleep
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP as oaep
from Crypto.Signature import pkcs1_15 as pkcs
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


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


def is_valid_aes_key(signature):
    sha256_hash = SHA256.new(AES_KEY)
    with open("security/public_key.pem", "rb") as file_pub:
        public_key = RSA.import_key(file_pub.read())

    try:
        print("\nValidating AES key...")
        pkcs.new(public_key).verify(sha256_hash, signature)
        print("Signed AES key is valid.")
        return True
    except (ValueError, TypeError) as ex:
        print(f"Invalid AES key: {ex}")
        return False


def send_message():
    message = str.encode("hello")

    aes_cipher = AES.new(AES_KEY, AES.MODE_CBC, IV)
    encrypted_message = aes_cipher.encrypt(pad(message, AES.block_size))
    server.send(encrypted_message)
    print(f"\nSent AES key encrypted message: {message.decode('utf-8')}")


def receive_message():
    message = server.recv(1024)
    print("\nReceived AES encrypyted message. Decrypting...")

    aes_cipher = AES.new(AES_KEY, AES.MODE_CBC, IV)
    decrypted_message = unpad(aes_cipher.decrypt(message), AES.block_size)
    decoded_message = decrypted_message.decode("utf-8")
    print(f"The decrypted message is: {decoded_message}")

    if decoded_message != "hello to you too":
        print("Received invalid message. Disconnecting...")
        exit(0)


if __name__ == "__main__":
    server = create_connection()
    initialize_handshake()
    sleep(3)

    signature = server.recv(1024)

    with open("security/aes_key", "rb") as f:
        AES_KEY = f.read()

    with open("security/iv", "rb") as f:
        IV = f.read()

    if not is_valid_aes_key(signature):
        print(f"\nAES key validation failed. Disconnecting from server...")
        exit(0)
    sleep(3)

    send_message()
    receive_message()

    sleep(3)
    print("\nDisconnecting client...")
    exit(0)
