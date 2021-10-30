import os
import hashlib
import pickle
import logging
from typing import Dict, List, NewType, Tuple, cast
from config import PBKDF2_HMAC_ITERATIONS, ROOT_PASSWORD, ROOT_USER
from model.database import Database
from model.persistent_dictionary import PersistentDictionary
from constants import DBS_OF_USERS_JSON_FILENAME, DBS_FILENAME, USERS_JSON_FILENAME, USERS_OF_DBS_JSON_FILENAME
from model.exception import DbAlreadyExistsError, DbNotExistError, UserNotExistError, UsernameAlreadyTakenError


DatabaseName = NewType('DatabaseName', str)
Username = NewType('Username', str)
KeyAndSalt = NewType('KeyAndSalt', bytes)


class Store():
  "Server wide object that stores the collection of users, databases and their relations."

  def __init__(self) -> None:
    self._dbs: Dict[DatabaseName, Database] = dict()
    self._users = PersistentDictionary[Username, str](filepath=USERS_JSON_FILENAME)
    self._users_of_dbs = PersistentDictionary[DatabaseName, Tuple[Username, ...]](filepath=USERS_OF_DBS_JSON_FILENAME)
    self._dbs_of_users = PersistentDictionary[Username, Tuple[DatabaseName, ...]](filepath=DBS_OF_USERS_JSON_FILENAME)
    try:
      self.create_user(Username(ROOT_USER), ROOT_PASSWORD)
      logging.info('registered root user from env vars')
    except BaseException:
      logging.info('root user was already registered')

  def delete_expired_keys_from_dbs(self) -> None:
    "Calls delete expired keys in all existing databses."
    for _, db in self._dbs.items():
      db.delete_expired_keys()

  def create_database(self, username: Username, new_db_name: DatabaseName) -> None:
    """
    Creates a new database with the given name if it did not exist earlier.
    Sets user as the owner of the database.
    """
    if new_db_name in self._dbs:
      raise DbAlreadyExistsError
    self._dbs[new_db_name] = Database()
    self._users_of_dbs[new_db_name] = tuple()
    self.add_user_to_owners(username=username, db_name=new_db_name)

  def add_user_to_owners(self, username: Username, db_name: DatabaseName) -> None:
    "Sets user as the owner of the specified database if it exists."
    if username not in self._users:
      raise UserNotExistError
    if username not in self._users_of_dbs[db_name]:
      self._users_of_dbs[db_name] = (username, *self._users_of_dbs[db_name])
      self._dbs_of_users[username] = (db_name, *self._dbs_of_users[username])

  def delete_database(self, username: Username, db_to_delete: DatabaseName) -> None:
    """
    Deletes the specified database if the user is an owner. Removes all
    ownership pertaining to this database before deletion.
    """
    if db_to_delete not in self._dbs or username not in self._users_of_dbs[db_to_delete]:
      return None
    del self._dbs[db_to_delete]
    db_users = self._users_of_dbs[db_to_delete]
    for db_user in db_users:
      self._dbs_of_users[db_user] = tuple(db for db in self._dbs_of_users[db_user] if db != db_to_delete)
    del self._users_of_dbs[db_to_delete]

  def delete_user(self, user_to_delete: Username) -> None:
    """
    If the specified user exists, then it get deleted, and removes
    user from the owner list of all databases.
    """
    if user_to_delete not in self._users:
      return None
    del self._users[user_to_delete]
    dbs_of_user = self._dbs_of_users[user_to_delete]
    for database in dbs_of_user:
      self._users_of_dbs[database] = tuple(user for user in self._users_of_dbs[database] if user != user_to_delete)
    del self._dbs_of_users[user_to_delete]

  def get_database_by_name(self, username: Username, db_name: DatabaseName) -> Database:
    "Returns a database if the specified user is within the owners of the database. Raises DbNotExistError otherwise."
    if db_name not in self._dbs or username not in self._users_of_dbs[db_name]:
      raise DbNotExistError
    return self._dbs[db_name]

  def _hash_password(self, password: bytes) -> KeyAndSalt:
    "Uses pbkdf2 hmac algorithm to hash a password iterations number of times."
    salt = os.urandom(32)
    # 100 000 iterations would prevent the server from responding for ~50ms since we run single threadedly
    key = hashlib.pbkdf2_hmac('sha256', password=password, salt=salt, iterations=PBKDF2_HMAC_ITERATIONS)
    return KeyAndSalt(key + salt)

  def _verify_password(self, password_to_verify: bytes, key_and_salt: bytes) -> bool:
    """
    Uses pbkdf2 hmac algorithm to hash the password to verify using a stored salt,
    then compares the new key with the stored one.
    """
    key = key_and_salt[:32]
    salt = key_and_salt[32:]
    key_to_verify = hashlib.pbkdf2_hmac('sha256', password=password_to_verify,
                                        salt=salt, iterations=PBKDF2_HMAC_ITERATIONS)
    return key_to_verify == key

  def create_user(self, username_to_create: Username, password: str) -> None:
    "Creates a new user if it does not exist already. Raises UsernameAlreadyTakenError otherwise."
    if username_to_create in self._users:
      raise UsernameAlreadyTakenError
    # TODO: check for invalid characters
    self._users[username_to_create] = self._hash_password(password.encode()).hex()
    self._dbs_of_users[username_to_create] = tuple()

  def authenticate_user(self, username: Username, password: str) -> bool:
    "Returns True if user with the provided username exists and the given password string is right."
    if username not in self._users:
      return False
    key_and_salt = bytes.fromhex(self._users[username])
    return self._verify_password(password_to_verify=password.encode(), key_and_salt=key_and_salt)

  def list_users_of_db(self, db_name: DatabaseName) -> List[Username]:
    "Retreives a list of usernames of whom the database is owned by."
    if db_name not in self._dbs:
      raise DbNotExistError
    return list(self._users_of_dbs[db_name])

  def list_dbs_of_user(self, username: Username) -> List[DatabaseName]:
    "Retreives a list of database names owned by the specified user."
    if username not in self._users:
      raise UserNotExistError
    return list(self._dbs_of_users[username])

  def load_dbs_from_disk(self) -> None:
    try:
      with open(DBS_FILENAME, 'rb') as file:
        self._dbs = pickle.load(file=file)
    except FileNotFoundError:
      logging.info(f'no {DBS_FILENAME} file found')
    else:
      logging.info(f'state loaded from {DBS_FILENAME}')

  def save_dbs_to_disk(self) -> None:
    with open(DBS_FILENAME, 'wb') as file:
      pickle.dump(self._dbs, file=file)
      logging.info(f'state saved in {DBS_FILENAME}')
