from typing import Dict
from model.exception import InvalidKeyError

Key = str
Value = str


class Database():
  _dictionary: Dict[Key, str] = dict()
  _ttl: Dict[str, int]

  def get(self, key: Key) -> Value:
    if key not in self._dictionary:
      raise InvalidKeyError
    return self._dictionary[key]

  def put(self, key: Key, value: Value) -> None:
    self._dictionary[key] = value

  def delete(self, key: Key) -> None:
    if key in self._dictionary:
      del self._dictionary[key]

  def update(self, key: Key, value: Value) -> None:
    if key not in self._dictionary:
      raise InvalidKeyError
    self._dictionary[key] = value
