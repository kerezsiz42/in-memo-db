from asyncio import StreamReader, StreamWriter
import logging
from user import authenticate_user

database = dict()

class BaseException(Exception):
  def __init__(self, message: str = ''):
    self.message = message
    super().__init__(self.message)
  
  def __str__(self):
    return f'{self.message}'

# update, ttl, current_db, select_db, new_db, delete_db, new_user, delete_user

class Session():
  def __init__(self):
    self._username = None
  
  @property
  def username(self):
    return self._username

  @username.setter
  def username(self, u):
    self._username = u

class Command():
  def login(self, session: Session, username='', password=''):
    if username == '' or password == '' or not authenticate_user(username, password):
      raise BaseException('invalid credentials')
    session.username = username
    return 'login: ok'

  def whoami(self, session: Session):
    return session.username

  def get(self, session: Session, key):
    if not session.username:
      raise BaseException('unauthorized')
    try:
      return database[key]
    except KeyError:
      raise BaseException('invalid key')

  def put(self, session: Session, key, value):
    if not session.username:
      raise BaseException('unauthorized')
    database[key] = value
    return 'put: ok'

  def delete(self, session: Session, key):
    if not session.username:
      raise BaseException('unauthorized')
    try:
      del database[key]
    except KeyError:
      pass
    return 'delete: ok'

  def execute_method(self, method):
    try:
      return getattr(self, method)
    except AttributeError:
      raise BaseException('invalid command')

async def handler(reader: StreamReader, writer: StreamWriter):
  session = Session()  
  while True:
    try:
      line = await reader.readline()
      if reader.at_eof():
        return
      command, *params = line.decode().rstrip().split(' ')
      # logs out user passwords, do not use this in production
      logging.info(f'message from client: {line}')

      response = Command().execute_method(command)(session, *params)
      
      writer.write(f'{response}\n'.encode())
    except BaseException as e:
      logging.warning(e)
      writer.write(f'{e}\n'.encode())
    await writer.drain()