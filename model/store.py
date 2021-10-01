
from typing import Dict, Set
import os
import hashlib
from config import PBKDF2_HMAC_ITERATIONS
from model.database import Database
from model.exception import BaseException

DatabaseName = str
Username = str
HashedPassword = bytes


class Store():
  def __init__(self):
    self._databases: Dict[DatabaseName, Database] = dict()
    self._users: Dict[Username, HashedPassword] = dict()
    self._users_of_databases: Dict[DatabaseName, Set[Username]] = dict()
    self._databases_of_users: Dict[Username, Set[DatabaseName]] = dict()

  # ttl
  # delete_db, delete_user
  def create_database(self, username: Username, new_db_name: DatabaseName):
    if username not in self._users:
      raise BaseException('user does not exist')
    if new_db_name in self._databases:
      raise BaseException('database already exist with the same name')
    self._databases[new_db_name] = Database()
    self._users_of_databases[new_db_name] = {username}
    self._databases_of_users[username].add(new_db_name)
    return 'create_db: ok'

  def get_database_by_name(self, username: Username, db_name: DatabaseName) -> Database:
    if db_name not in self._databases or username not in self._users_of_databases[db_name]:
      raise BaseException('database does not exist')
    return self._databases[db_name]

  def _hash_password(self, password: bytes) -> bytes:
    salt = os.urandom(32)
    # 100 000 iterations would prevent the server from responding for ~50ms since we run single threadedly
    key = hashlib.pbkdf2_hmac('sha256', password=password, salt=salt, iterations=PBKDF2_HMAC_ITERATIONS)
    return key + salt

  def _verify_password(self, password_to_verify: bytes, key_and_salt: bytes) -> bool:
    key = key_and_salt[:32]
    salt = key_and_salt[32:]
    key_to_verify = hashlib.pbkdf2_hmac('sha256', password=password_to_verify,
                                        salt=salt, iterations=PBKDF2_HMAC_ITERATIONS)
    return key_to_verify == key

  def create_user(self, username: str, password: str) -> str:
    if username in self._users:
      raise BaseException('username already taken')
    self._users[username] = self._hash_password(password.encode())
    self._databases_of_users[username] = set()
    return 'register: ok'

  def authenticate_user(self, username: str, password: str) -> bool:
    if username not in self._users:
      return False
    key_and_salt = self._users[username]
    return self._verify_password(password_to_verify=password.encode(), key_and_salt=key_and_salt)
