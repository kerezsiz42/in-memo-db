from typing import Dict
import time
from model.exception import InvalidKeyError

Key = str
Value = str
ExpireAtEpoch = int
TTL = int


class Database():
  _dictionary: Dict[Key, str] = dict()
  _expire_at_epoch_by_keys: Dict[Key, ExpireAtEpoch] = dict()

  def delete_expired_keys(self) -> None:
    # https://stackoverflow.com/questions/5384914/how-to-delete-items-from-a-dictionary-while-iterating-over-it
    # We create a list from the iterable keys in order to prevent RuntimeError from getting raised,
    # since we don't care whether the dictionary changes size during iteration.
    for key in list(self._expire_at_epoch_by_keys.keys()):
      if int(time.time()) > self._expire_at_epoch_by_keys[key]:
        self.delete(key=key)
        self.remove_ttl(key=key)

  def remove_ttl(self, key: Key) -> None:
    self._expire_at_epoch_by_keys.pop(key, None)

  def set_ttl(self, key: Key, ttl: TTL) -> None:
    self._expire_at_epoch_by_keys[key] = int(time.time()) + ttl

  def get(self, key: Key) -> Value:
    try:
      return self._dictionary[key]
    except KeyError:
      raise InvalidKeyError

  def put(self, key: Key, value: Value) -> None:
    self._dictionary[key] = value

  def delete(self, key: Key) -> None:
    self._dictionary.pop(key, None)

  def update(self, key: Key, value: Value) -> None:
    if key not in self._dictionary:
      raise InvalidKeyError
    self._dictionary[key] = value
