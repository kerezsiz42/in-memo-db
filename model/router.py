import os
from typing import Callable, Dict, List
from asyncio import StreamReader, StreamWriter
import logging
from config import ROOT_USER
from enum import Enum, unique
from constants import SEQUENTIAL_SAVE_FILENAME
from model.context import Context
from model.database import Database
from model.exception import CustomException, InvalidCommandError
from model.store import DatabaseName, Store
from model.custom_time import custom_time
from handlers import add_user_to_owners, create_db, register_user, current_db, delete, delete_db
from handlers import get, list_dbs, list_users, login, put, select_db, update, whoami, delete_user


@unique
class Route(Enum):
  login = 'login'
  whoami = 'whoami'
  register_user = 'register_user'
  add_user_to_owners = 'add_user_to_owners'
  create_db = 'create_db'
  select_db = 'select_db'
  delete_db = 'delete_db'
  delete_user = 'delete_user'
  list_users = 'list_users'
  list_dbs = 'list_dbs'
  current_db = 'current_db'
  get = 'get'
  put = 'put'
  delete = 'delete'
  update = 'update'


Handler = Callable[[Context], str]


class Router():
  "Stores routes and runs the appropiate handlers when called."

  def __init__(self, store: Store):
    self._store: Store = store
    self._routes: Dict[Route, List[Handler]] = {
        Route.login: [login],
        Route.whoami: [whoami],
        Route.register_user: [register_user],
        Route.add_user_to_owners: [whoami, add_user_to_owners],
        Route.create_db: [whoami, create_db],
        Route.select_db: [whoami, select_db],
        Route.delete_db: [whoami, delete_db],
        Route.delete_user: [whoami, delete_user],
        Route.list_users: [whoami, list_users],
        Route.list_dbs: [whoami, list_dbs],
        Route.current_db: [whoami, current_db],
        Route.get: [whoami, current_db, get],
        Route.put: [whoami, current_db, put],
        Route.delete: [whoami, current_db, delete],
        Route.update: [whoami, current_db, update]
    }

  async def __call__(self, reader: StreamReader, writer: StreamWriter) -> None:
    """
    Handles the communication between server and client through
    the read and write streams provided by asyncio.start_server()
    It parses input line by line and calls the appropriate handlers
    in order if they where defined for the route provided by the user.
    """
    logging.info('new client connected')
    ctx = Context(store=self._store)
    while True:
      response = None
      line = await reader.readline()
      if reader.at_eof():
        logging.info('client closed connection')
        break
      route_str, *params = line.decode().rstrip().split()

      ctx.params = params
      try:
        try:
          route = Route[route_str]
        except KeyError:
          raise InvalidCommandError
        for handler in self._routes[route]:
          response = handler(ctx)
      except CustomException as err:
        logging.warning(err)
        response = str(err)
      except Exception as err:
        logging.warning(err)
        print(err)
        response = 'internal server error'
      else:
        self.try_to_save_successful_command(ctx.database_name, route, params)
      finally:
        writer.write(f'{response}\n'.encode())
        await writer.drain()

  def load_sequential_save_file(self) -> None:
    try:
      with open(SEQUENTIAL_SAVE_FILENAME, 'r') as file:
        for line in file:
          exec_time_str, command_str_with_db_name, = line.rstrip().split('\t')
          custom_time.time = int(exec_time_str)
          route_str, *params = command_str_with_db_name.split()
          route = Route[route_str]

          try:
            if route in [Route.delete, Route.put, Route.update]:
              db_name, *params = params
              database: Database = self._store.get_database_by_name(username=ROOT_USER, db_name=db_name)
              if route == Route.delete:
                database.delete(key=params[0])
              elif route == Route.put:
                database.put(key=params[0], value=params[1])
              elif route == Route.update:
                database.update(key=params[0], value=params[1])
            elif route == Route.create_db:
              self._store.create_database(new_db_name=params[0], username=ROOT_USER)
            elif route == Route.delete_db:
              self._store.delete_database(db_to_delete=params[0], username=ROOT_USER)
          except CustomException as err:
            logging.warning(f'cannot execute command from past: {err}')

        custom_time.time = None
        self._store.delete_expired_keys_from_dbs()
    except FileNotFoundError:
      logging.info(f'no {SEQUENTIAL_SAVE_FILENAME} file found')
    else:
      logging.info(f'loaded {SEQUENTIAL_SAVE_FILENAME}')
      self.delete_sequential_save_file()

  def delete_sequential_save_file(self) -> None:
    try:
      os.remove(SEQUENTIAL_SAVE_FILENAME)
    except OSError:
      logging.info(f'no {SEQUENTIAL_SAVE_FILENAME} file found')
    else:
      logging.info(f'deleted {SEQUENTIAL_SAVE_FILENAME}')

  def try_to_save_successful_command(self, database_name: DatabaseName, route: Route, params: List[str]) -> None:
    command = None
    if route == Route.delete:
      key = params[0]
      command = [route.value, database_name, key]
    elif route in [Route.put, Route.update]:
      key = params[0]
      value = params[1]
      command = [route.value, database_name, key, value]
      try:
        ttl_string = params[2]
        command.append(ttl_string)
      except IndexError:
        pass
    elif route in [Route.delete_db, Route.create_db]:
      db_name = params[0]
      command = [route.value, db_name]
    if command is not None:
      with open(SEQUENTIAL_SAVE_FILENAME, 'a') as file:
        file.write(f'{custom_time.time}\t{" ".join(command)}\n')
