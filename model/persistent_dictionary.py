import json
import os
from typing import Dict, Iterator, TypeVar

K = TypeVar('K', str, int)
V = TypeVar('V', str, int, list, dict)
FileDictionary = Dict[K, V]


class PersistentDictionary():
  def __init__(self, filepath):
    self._filepath = filepath
    self._dict: FileDictionary = dict()
    file_exists = os.path.isfile(self._filepath)
    if not file_exists or (file_exists and os.path.getsize(self._filepath) == 0):
      self._write_file(obj=self._dict)
    else:
      self._dict = self._read_file()

  def _read_file(self) -> FileDictionary:
    with open(self._filepath, 'r') as file:
      obj = json.load(fp=file)
      return obj

  def _write_file(self, obj: FileDictionary) -> None:
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

  def __iter__(self) -> Iterator:
    return iter(self._dict)
