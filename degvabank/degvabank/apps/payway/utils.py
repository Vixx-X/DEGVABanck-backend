import secrets
from cryptography.fernet import Fernet

def gen_key_pair():
    return secrets.token_urlsafe(33), Fernet.generate_key().decode("utf8")


def encrypt(key, msg):
    f = Fernet(key.encode("utf8"))
    return f.encrypt(msg.encode("utf8"))


def decrypt(key, msg):
    f = Fernet(key.encode("utf8"))
    return f.decrypt(msg).decode("utf8")


def censor_key(key):
    return f"*********{key[-5:]}"

