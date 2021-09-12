import hashlib
import os

users = dict()

def hash_password(password: bytes) -> bytes:
  salt = os.urandom(32)
  key = hashlib.pbkdf2_hmac('sha256', password=password, salt=salt, iterations=10_000)
  return key + salt

def verify_password(password_to_verify: bytes, key_and_salt: bytes) -> bool:
  key = key_and_salt[:32]
  salt = key_and_salt[32:]
  key_to_verify = hashlib.pbkdf2_hmac('sha256', password=password_to_verify, salt=salt, iterations=10_000)
  return key_to_verify == key

def register_user(username: str, password: str) -> bool:
  if username in users:
    return False
  users[username] = hash_password(password.encode())
  return True

def authenticate_user(username: str, password: str) -> bool:
  if username not in users:
    return False
  key_and_salt = users[username]
  return verify_password(password_to_verify=password.encode(), key_and_salt=key_and_salt)

register_user(os.environ['ROOT_USER'], os.environ['ROOT_PASSWORD'])
