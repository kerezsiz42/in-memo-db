from typing import Dict
from model.exception import BaseException


class Database():
  _dictionary: Dict[str, str] = dict()

  def get(self, key: str) -> str:
    if key in self._dictionary:
      return self._dictionary[key]
    else:
      raise BaseException('invalid key')

  def put(self, key: str, value: str) -> str:
    self._dictionary[key] = value
    return 'put: ok'

  def delete(self, key: str) -> str:
    if key in self._dictionary:
      del self._dictionary[key]
    return 'delete: ok'

  def update(self, key: str, value: str) -> str:
    if key in self._dictionary:
      self._dictionary[key] = value
      return 'update: ok'
    else:
      raise BaseException('invalid key')
