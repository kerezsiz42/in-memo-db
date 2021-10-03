from typing import List, Optional
from model.store import DatabaseName, Store, Username
from model.database import Database


class Context():
  def __init__(self, username: Username, database_name: DatabaseName, database: Optional[Database], store: Store, params: List[str]):
    self._username = username
    self._database_name = database_name
    self._database = database
    self._store = store
    self._params = params

  @property
  def username(self):
    return self._username

  @username.setter
  def username(self, username: Username):
    self._username = username

  @property
  def database_name(self):
    return self._database_name

  @database_name.setter
  def database_name(self, database_name: DatabaseName):
    self._database_name = database_name

  @property
  def database(self):
    return self._database

  @database.setter
  def database(self, database: Database):
    self._database = database

  @property
  def store(self):
    return self._store

  @property
  def params(self):
    return self._params

  @params.setter
  def params(self, params: List[str]):
    self._params = params
