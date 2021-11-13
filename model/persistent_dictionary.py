import json
import os
from typing import Dict, Generic, Iterator, Tuple, TypeVar, cast

K = TypeVar('K', str, int)
# immutable types only
V = TypeVar('V', str, Tuple[str, ...])


class PersistentDictionary(Generic[K, V]):
  '''
  A dict() like object whose properties can be set, deleted,
  iterated through and read which writes every change into a json file.
  '''

  def __init__(self, filepath: str) -> None:
    self._filepath = filepath
    self._dict: Dict[K, V] = dict()
    file_exists = os.path.isfile(self._filepath)
    if not file_exists:
      self._write_file(obj=self._dict)
    else:
      self._dict = self._read_file()

  def _read_file(self) -> Dict[K, V]:
    with open(self._filepath, 'r') as file:
      return cast(Dict[K, V], json.load(fp=file))

  def _write_file(self, obj: Dict[K, V]) -> None:
    with open(self._filepath, 'w') as file:
      json.dump(obj=obj, fp=file)

  def __getitem__(self, key: K) -> V:
    return self._dict[key]

  def __setitem__(self, key: K, value: V) -> None:
    self._dict[key] = value
    self._write_file(obj=self._dict)

  def __delitem__(self, key: K) -> None:
    del self._dict[key]
    self._write_file(obj=self._dict)

  def __iter__(self) -> Iterator[K]:
    return iter(self._dict)
