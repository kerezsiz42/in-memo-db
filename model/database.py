from typing import Dict
import time
from model.exception import InvalidKeyError

Key = str
Value = str
ExpireAtEpoch = int
TTL = int


class Database():
  """Single self-contained storage object that the user can select and manipulate through the handlers."""

  def __init__(self):
    self._dictionary: Dict[Key, str] = dict()
    self._expire_at_epoch_by_keys: Dict[Key, ExpireAtEpoch] = dict()

  def delete_expired_keys(self) -> None:
    """Iterates through keys that have expiration to call the delete and remove methods on them."""
    # We create a list from the iterable keys in order to prevent RuntimeError from getting raised,
    # since we don't care whether the dictionary changes size during iteration.
    for key in list(self._expire_at_epoch_by_keys.keys()):
      if int(time.time()) > self._expire_at_epoch_by_keys[key]:
        self.delete(key=key)
        self.remove_ttl(key=key)

  def remove_ttl(self, key: Key) -> None:
    """Removes a key from the expiration tracker dictionary."""
    self._expire_at_epoch_by_keys.pop(key, None)

  def set_ttl(self, key: Key, ttl: TTL) -> None:
    """Updates or sets the new expiration time for the given key to current time + ttl seconds."""
    self._expire_at_epoch_by_keys[key] = int(time.time()) + ttl

  def get(self, key: Key) -> Value:
    """Returns the value stored under the specified key from the database.
    If desired key does not exist, then raises InvalidKeyError."""
    if key not in self._dictionary:
      raise InvalidKeyError
    return self._dictionary[key]

  def put(self, key: Key, value: Value) -> None:
    """Set value under the specified key even if it did not exist earlier."""
    self._dictionary[key] = value

  def delete(self, key: Key) -> None:
    """If key exist in database then it gets deleted, otherwise nothing happens."""
    self._dictionary.pop(key, None)

  def update(self, key: Key, value: Value) -> None:
    """Set value under the specified key only if it existed before."""
    if key not in self._dictionary:
      raise InvalidKeyError
    self._dictionary[key] = value
