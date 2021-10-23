from typing import List, Optional
from model.store import DatabaseName, Store, Username
from model.database import Database


class Context():
  "A temporary storage for the connected clients to store their state during the lifetime of the connection."

  def __init__(self, username: Username, database_name: DatabaseName, database: Optional[Database], store: Store, params: List[str]):
    self._username = username
    self._database_name = database_name
    self._database = database
    self._store = store
    self._params = params

  @property
  def username(self) -> Username:
    "Returns the username string stored in the context object."
    return self._username

  @username.setter
  def username(self, username: Username) -> None:
    "Set the username string stored in the context object."
    self._username = username

  @property
  def database_name(self) -> DatabaseName:
    "Returns the database name string stored in the context object."
    return self._database_name

  @database_name.setter
  def database_name(self, database_name: DatabaseName) -> None:
    "Set the database name string stored in the context object."
    self._database_name = database_name

  @property
  def database(self) -> Database:
    "Returns the database object stored in the context object."
    return self._database

  @database.setter
  def database(self, database: Database) -> None:
    "Set the database object stored in the context object."
    self._database = database

  @property
  def store(self) -> Store:
    "Returns the store object stored in the context object."
    return self._store

  @property
  def params(self) -> List[str]:
    "Returns the list of string parameters provided by the user after the command name."
    return self._params

  @params.setter
  def params(self, params: List[str]):
    "Sets the list of string parameters provided by the user after the command name."
    self._params = params
