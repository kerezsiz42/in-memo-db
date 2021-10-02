from typing import Any, Callable, Dict, List
from asyncio import StreamReader, StreamWriter
import logging
from model.store import Store

Context = Dict[str, Any]
Handler = Callable[[Context], str]


class Router():
  def __init__(self):
    self._routes: Dict[str, List[Handler]] = dict()

  def use(self, route: str, handler_list: List[Handler]):
    self._routes[route] = handler_list
    return self

  async def __call__(self, reader: StreamReader, writer: StreamWriter, store: Store):
    ctx: Context = dict(username=str(), database_name=str(), database=None, store=store, params=list())
    while True:
      response = str()
      try:
        # What happens when connection is reset by peer?
        line = await reader.readline()
        if reader.at_eof():
          return
        route, *params = line.decode().rstrip().split()
        ctx['params'] = params
        if route in self._routes:
          for handler in self._routes[route]:
            response = handler(ctx)
        else:
          raise BaseException('invalid command')
      except BaseException as err:
        logging.warning(err)
        response = str(err)
      finally:
        writer.write(f'{response}\n'.encode())
        await writer.drain()
