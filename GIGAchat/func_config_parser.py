import configparser


def get_auth() -> str:
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config["GIGACHAT"]["auth"]
