from asyncio import StreamReader, StreamWriter
import logging
from model.session import Session
from model.store import Store
from model.exception import BaseException


def params_validator(params, n):
  if len(params) < n:
    raise BaseException('invalid number of parameters')


async def handler(reader: StreamReader, writer: StreamWriter, store: Store):
  session = Session()
  while True:
    res = None
    try:
      # What happens when connection is reset by peer?
      line = await reader.readline()
      if reader.at_eof():
        return
      command, *params = line.decode().rstrip().split(' ')

      if command == 'login':
        params_validator(params, 2)
        res = session.login(store=store, username=params[0], password=params[1])
      elif command == 'whoami':
        res = session.whoami()
      elif command == 'create_db':
        params_validator(params, 1)
        res = store.create_database(username=session.whoami(), new_db_name=params[0])
      elif command == 'select_db':
        params_validator(params, 1)
        res = session.select_db(store=store, db_name=params[0])
      elif command == 'current_db':
        res = session.current_db()
      elif command == 'get':
        params_validator(params, 1)
        res = store.get_database_by_name(username=session.whoami(), db_name=session.current_db()).get(key=params[0])
      elif command == 'put':
        params_validator(params, 2)
        res = store.get_database_by_name(username=session.whoami(
        ), db_name=session.current_db()).put(key=params[0], value=params[1])
      elif command == 'delete':
        params_validator(params, 1)
        res = store.get_database_by_name(username=session.whoami(), db_name=session.current_db()).delete(key=params[0])
      elif command == 'update':
        params_validator(params, 2)
        res = store.get_database_by_name(username=session.whoami(
        ), db_name=session.current_db()).update(key=params[0], value=params[1])
      else:
        raise BaseException('invalid command')
    except BaseException as err:
      logging.warning(err)
      res = str(err)
    finally:
      writer.write(f'{res}\n'.encode())
      await writer.drain()
