import time
from typing import Optional


class CustomTime():
  def __init__(self) -> None:
    self._time: Optional[int] = None

  @property
  def time(self) -> int:
    return int(time.time()) if self._time is None else self._time

  @time.setter
  def time(self, time: Optional[int]) -> None:
    self._time = time


custom_time = CustomTime()
