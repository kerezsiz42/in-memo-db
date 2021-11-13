import time
from typing import Optional


class CustomTime():
  'A time object that can be manipulated to go back or forward in time.'

  def __init__(self) -> None:
    self._time: Optional[int] = None

  @property
  def time(self) -> int:
    'Returns current time or a mocked time as an epoch integer.'
    return int(time.time()) if self._time is None else self._time

  @time.setter
  def time(self, time: Optional[int]) -> None:
    'Sets time attribute to the given integer or None.'
    self._time = time


custom_time = CustomTime()
