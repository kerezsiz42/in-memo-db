from typing import Callable, Dict, List
from asyncio import StreamReader, StreamWriter
import logging
from model.context import Context
from model.exception import InternalServerError, InvalidCommandError
from model.store import Store


Handler = Callable[[Context], str]


class Router():
  "Stores routes and runs the appropiate handlers when called."

  def __init__(self, store: Store):
    self._routes: Dict[str, List[Handler]] = dict()
    self._store: Store = store

  def use(self, route: str, handler_list: List[Handler]):
    "Sets a list of handlers pertaining to this route name of the router object."
    self._routes[route] = handler_list
    return self

  async def __call__(self, reader: StreamReader, writer: StreamWriter):
    """
    Handles the communication between server and client through
    the read and write streams provided by asyncio.start_server()
    It parses input line by line and calls the appropriate handlers
    in order if they where defined for the route provided by the user.
    """
    logging.info('new client connected')
    ctx = Context(username=str(), database_name=str(), database=None, store=self._store, params=list())
    while True:
      response = None
      line = await reader.readline()
      if reader.at_eof():
        logging.info('client closed connection')
        return
      stripped_decoded_line = line.decode().rstrip()
      route, *params = stripped_decoded_line.split()
      ctx.params = params
      try:
        if route not in self._routes:
          raise InvalidCommandError
        last_index = len(self._routes[route]) - 1
        for index, handler in enumerate(self._routes[route]):
          if index == last_index:
            response = handler(ctx)
          else:
            handler(ctx)
        if response == None:
          raise InternalServerError
        self._store.append_successful_command(stripped_decoded_line)
      except BaseException as err:
        logging.warning(err)
        response = str(err)
      finally:
        writer.write(f'{response}\n'.encode())
        await writer.drain()
