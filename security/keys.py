from Crypto.PublicKey import RSA


def generate_keys():
    print("Generating public and private keys...")
    key = RSA.generate(2048)

    with open("security/private_key.pem", "wb") as f_priv:
        f_priv.write(key.export_key("PEM"))

    with open("security/public_key.pem", "wb") as f_pub:
        f_pub.write(key.public_key().export_key("PEM"))
