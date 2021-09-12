from asyncio import StreamReader, StreamWriter
import logging
from enum import Enum, unique
from user import authenticate_user, users

database = dict()

class BaseException(Exception):
  def __init__(self, message: str = ''):
    self.message = message
    super().__init__(self.message)
  
  def __str__(self):
    return f'{self.message}'

@unique
class CommandType(Enum):
  # User commands
  login = 'login' # anyone
  whoami = 'whoami' # anyone
  new_user = 'new_user' # anyone
  delete_user = 'remove_user' # themselves or root, deletes their databases
  exit = 'exit' # anyone
  # Database commands
  current_db = 'current_db'
  select_db = 'select_db' # root can select any
  new_db = 'new_db' # anyone
  delete_db = 'delete_db' # root can delete any
  # Entity commands
  put = 'put'
  get = 'get'
  update = 'update'
  delete = 'delete'
  ttl = 'ttl'

async def handler(reader: StreamReader, writer: StreamWriter):
  current_user = None
  while True:
    try:
      line = await reader.readline()
      message = line.decode().rstrip().split(' ')

      # logs out user passwords, do not use this in production
      logging.info(f'message from client: {line}')
      response_string = str()
      command = message[0]
      
      if command == CommandType.login.value:
        if len(message) < 3 or not authenticate_user(message[1], message[2]):
          raise BaseException('invalid credentials')
        current_user = message[1]
        response_string = 'login: ok'
      elif command == CommandType.exit.value:
        writer.close()
        logging.info('connection closed with client')
        return
      elif command == CommandType.whoami.value:
        response_string = current_user
      elif current_user in users:
        if command == CommandType.get.value:
          try:
            response_string = database[message[1]]
          except KeyError:
            raise BaseException('invalid key')
        elif command == CommandType.put.value:
          database[message[1]] = message[2]
          response_string = 'put: ok'
        elif command == CommandType.delete.value:
          try:
            del database[message[1]]
          except KeyError:
            pass
          finally:
            response_string = 'delete: ok'
      else:
        raise BaseException('invalid command or unauthorized user')
      writer.write(f'{response_string}\n'.encode())
      await writer.drain()
    except BaseException as e:
      logging.warning(e)
      writer.write(f'{e}\n'.encode())
      await writer.drain()