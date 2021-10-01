from model.store import DatabaseName, Store
from model.exception import BaseException


class Session():
  def __init__(self):
    self._username: str = str()
    self._database_name: str = str()

  def whoami(self) -> str:
    if len(self._username) == 0:
      raise BaseException('you must be logged in')
    return self._username

  def current_db(self):
    if len(self._database_name) == 0:
      raise BaseException('no database selected')
    return self._database_name

  def login(self, store: Store, username: str = str(), password: str = str()) -> str:
    if len(username) == 0 or len(password) == 0 or not store.authenticate_user(username, password):
      raise BaseException('invalid credentials')
    self._username = username
    self._database_name = str()
    return 'login: ok'

  def select_db(self, store: Store, db_name: DatabaseName) -> str:
    store.get_database_by_name(username=self.whoami(), db_name=db_name)
    self._database_name = db_name
    return 'select_db: ok'
