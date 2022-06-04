import yaml


def get_credentials():
    try:
        with open("security/credentials.yml", "r") as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as ex:
        print(f"Error occured while loading credentials config: {ex}")
