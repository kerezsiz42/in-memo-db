from typing import Tuple
from model.route import Route
from model.exception import InvalidCommandError


def validate_route(line: bytes) -> Tuple[Route, Tuple[str, ...]]:
  route_str, *params = line.decode().rstrip().split()
  try:
    route = Route[route_str]
  except KeyError:
    raise InvalidCommandError
  return (route, tuple(params))
