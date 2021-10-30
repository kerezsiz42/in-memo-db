from typing import Tuple
from model.route import Route
from model.exception import InvalidCommandError


def validate_route(line: bytes) -> Tuple[Route, Tuple[str, ...]]:
  'Validates raw bytes and returns a route object and a string tuple containing the params.'
  route_str, *params = line.decode().rstrip().split()
  if len(params) > 4:
    raise InvalidCommandError
  try:
    route = Route[route_str]
  except KeyError:
    raise InvalidCommandError
  return (route, tuple(params))
