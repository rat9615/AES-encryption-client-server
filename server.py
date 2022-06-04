import socket
from utils import util
from time import sleep
from security.keys import generate_keys
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP as oaep
from Crypto.Signature import pkcs1_15 as pkcs
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def bind_connection():
    port = int(input("Enter the port you want the socket to bind to:\t"))
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((socket.gethostname(), port))
    server.listen(1)
    print(f"Listening to connections on port: {port}")
    return server


def decrypt_password(message):
    with open("security/private_key.pem", "rb") as file_priv:
        key = RSA.import_key(file_priv.read())
    decrypted_password = oaep.new(key).decrypt(message)
    return decrypted_password.decode("utf-8")


def is_handshake_complete():
    message = client.recv(1024)
    dcrypt_message = decrypt_password(message)
    print(f"Secret password is: {dcrypt_message}")
    credentials = util.get_credentials()
    if dcrypt_message != credentials['app']['password']:
        print("Handshake failed. Disconnecting from client")
        return False
    print("Handshake successful!")
    return True


def generate_signed_aes_key():
    with open("security/private_key.pem", "rb") as file_pub:
        private_key = RSA.import_key(file_pub.read())

    sha256_hash = SHA256.new(AES_KEY)
    aes_sign_key = pkcs.new(private_key).sign(sha256_hash)
    return aes_sign_key


def send_message():
    message = str.encode("hello to you too")
    aes_cipher = AES.new(AES_KEY, AES.MODE_CBC, IV)
    encrypted_message = aes_cipher.encrypt(pad(message, AES.block_size))
    client.send(encrypted_message)
    print(f"\nSent AES key encrypted message: {message.decode('utf-8')}")


def receive_message():
    message = client.recv(1024)
    print("\nReceived AES encrypyted message. Decrypting...")

    aes_cipher = AES.new(AES_KEY, AES.MODE_CBC, IV)
    decrypted_message = unpad(aes_cipher.decrypt(message), AES.block_size)
    decoded_message = decrypted_message.decode("utf-8")
    print(f"The decrypted message is: {decoded_message}")

    if decoded_message != "hello":
        print("Invalid message. Disconnecting...")
        server.shutdown(socket.SHUT_RDWR)
        server.close()
        exit(0)


if __name__ == "__main__":
    generate_keys()
    server = bind_connection()

    while True:
        client, address = server.accept()
        print(f"\nEstablished connection request from client: {address}")

        if not is_handshake_complete():
            server.shutdown(socket.SHUT_RDWR)
            server.close()
            exit(0)

        print("\nSending signed AES key to client...")
        AES_KEY = util.generate_aes_key()
        IV = util.generate_iv()
        aes_signed_key = generate_signed_aes_key()
        client.send(aes_signed_key)

        receive_message()
        sleep(3)

        send_message()
        sleep(3)
        print("\nShutting down server...")
        server.shutdown(socket.SHUT_RDWR)
        server.close()
        exit(0)
