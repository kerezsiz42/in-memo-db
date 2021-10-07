
from typing import Dict, Set
import os
import hashlib
from config import PBKDF2_HMAC_ITERATIONS
from model.database import Database
from model.exception import DbAlreadyExistsError, DbNotExistError, UserNotExistError, UsernameAlreadyTakenError

DatabaseName = str
Username = str
HashedPassword = bytes


class Store():
  def __init__(self):
    self._dbs: Dict[DatabaseName, Database] = dict()
    self._users: Dict[Username, HashedPassword] = dict()
    self._users_of_dbs: Dict[DatabaseName, Set[Username]] = dict()
    self._dbs_of_users: Dict[Username, Set[DatabaseName]] = dict()

  def create_database(self, username: Username, new_db_name: DatabaseName) -> None:
    if username not in self._users:
      raise UserNotExistError
    if new_db_name in self._dbs:
      raise DbAlreadyExistsError
    self._dbs[new_db_name] = Database()
    self.add_user_to_owners(username=username, db_name=new_db_name)

  def add_user_to_owners(self, username: Username, db_name: DatabaseName) -> None:
    if username not in self._users:
      raise UserNotExistError
    self._users_of_dbs[db_name] = {username}
    self._dbs_of_users[username].add(db_name)

  def delete_database(self, username: Username, db_to_delete: DatabaseName) -> None:
    if db_to_delete not in self._dbs or username not in self._users_of_dbs[db_to_delete]:
      # idempotency
      return None
    del self._dbs[db_to_delete]
    db_users = self._users_of_dbs[db_to_delete]
    for db_user in db_users:
      databases_of_user = self._dbs_of_users[db_user]
      databases_of_user.remove(db_to_delete)
    del self._users_of_dbs[db_to_delete]

  def delete_user(self, user_to_delete: Username) -> None:
    if user_to_delete not in self._users:
      # idempotency
      return None
    del self._users[user_to_delete]
    dbs_of_user = self._dbs_of_users[user_to_delete]
    for database in dbs_of_user:
      users_of_db = self._users_of_dbs[database]
      users_of_db.remove(user_to_delete)
    del self._dbs_of_users[user_to_delete]

  def get_database_by_name(self, username: Username, db_name: DatabaseName) -> Database:
    if db_name not in self._dbs or username not in self._users_of_dbs[db_name]:
      raise DbNotExistError
    return self._dbs[db_name]

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

  def create_user(self, username_to_create: str, password: str) -> None:
    if username_to_create in self._users:
      raise UsernameAlreadyTakenError
    self._users[username_to_create] = self._hash_password(password.encode())
    self._dbs_of_users[username_to_create] = set()

  def authenticate_user(self, username: str, password: str) -> bool:
    if username not in self._users:
      return False
    key_and_salt = self._users[username]
    return self._verify_password(password_to_verify=password.encode(), key_and_salt=key_and_salt)

  def list_users_of_db(self, db_name: DatabaseName) -> Set[DatabaseName]:
    if db_name not in self._dbs:
      raise DbNotExistError
    return self._users_of_dbs[db_name]

  def list_dbs_of_user(self, username: Username) -> Set[Username]:
    if username not in self._users:
      raise UserNotExistError
    return self._dbs_of_users[username]
