import yaml
from Crypto.Random import get_random_bytes


def get_credentials():
    try:
        with open("security/credentials.yml", "r") as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as ex:
        print(f"Error occured while loading credentials config: {ex}")


# ! Any alternate way to do this in a single pass.
# ! and without saving the key


def generate_aes_key():
    with open("security/aes_key", "wb") as f:
        key = get_random_bytes(16)
        f.write(key)
    return key


def generate_iv():
    with open("security/iv", "wb") as f:
        iv = get_random_bytes(16)
        f.write(iv)
    return iv
