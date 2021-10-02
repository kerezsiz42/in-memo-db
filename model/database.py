from typing import Dict
from model.exception import BaseException


class Database():
  _dictionary: Dict[str, str] = dict()

  def get(self, key: str) -> str:
    if key not in self._dictionary:
      raise BaseException('invalid key')
    return self._dictionary[key]

  def put(self, key: str, value: str) -> None:
    self._dictionary[key] = value

  def delete(self, key: str) -> None:
    if key in self._dictionary:
      del self._dictionary[key]

  def update(self, key: str, value: str) -> None:
    if key not in self._dictionary:
      raise BaseException('invalid key')
    self._dictionary[key] = value
