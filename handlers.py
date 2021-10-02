from config import ROOT_USER
from model.database import Database
from model.router import Context
from model.store import DatabaseName, Store, Username


def login(ctx: Context) -> str:
  try:
    username, password = ctx['params']
  except ValueError:
    raise BaseException('invalid number of parameters')
  store: Store = ctx['store']
  if len(username) == 0 or len(password) == 0 or not store.authenticate_user(username, password):
    raise BaseException('invalid credentials')
  ctx['username'] = username
  ctx['database_name'] = str()
  ctx['database'] = None
  return 'login: ok'


def whoami(ctx: Context) -> str:
  username: Username = ctx['username']
  if len(username) == 0:
    raise BaseException('you must be logged in')
  return username


def create_db(ctx: Context) -> str:
  try:
    new_db_name, = ctx['params']
  except ValueError:
    raise BaseException('invalid number of parameters')
  store: Store = ctx['store']
  username: Username = ctx['username']
  store.create_database(username=username, new_db_name=new_db_name)
  store.add_user_to_owners(username=ROOT_USER, db_name=new_db_name)
  return 'create_db: ok'


def select_db(ctx: Context) -> str:
  try:
    db_name, = ctx['params']
  except ValueError:
    raise BaseException('invalid number of parameters')
  store: Store = ctx['store']
  username: Username = ctx['username']
  selected_db = store.get_database_by_name(username=username, db_name=db_name)
  ctx['database'] = selected_db
  ctx['database_name'] = db_name
  return 'select_db: ok'


def current_db(ctx: Context) -> str:
  database_name: DatabaseName = ctx['database_name']
  if len(database_name) == 0:
    raise BaseException('no database selected')
  return database_name


def get(ctx: Context) -> str:
  try:
    key, = ctx['params']
  except ValueError:
    raise BaseException('invalid number of parameters')
  db: Database = ctx['database']
  return db.get(key=key)


def put(ctx: Context) -> str:
  try:
    key, value = ctx['params']
  except ValueError:
    raise BaseException('invalid number of parameters')
  db: Database = ctx['database']
  db.put(key=key, value=value)
  return 'put: ok'


def delete(ctx: Context) -> str:
  try:
    key, = ctx['params']
  except ValueError:
    raise BaseException('invalid number of parameters')
  db: Database = ctx['database']
  db.delete(key=key)
  return 'delete: ok'


def update(ctx: Context) -> str:
  try:
    key, value = ctx['params']
  except ValueError:
    raise BaseException('invalid number of parameters')
  db: Database = ctx['database']
  db.update(key=key, value=value)
  return 'update: ok'


def delete_user(ctx: Context) -> str:

  return 'delete_user: ok'


def delete_db(ctx: Context) -> str:

  return 'delete_db: ok'


def create_user(ctx: Context) -> str:

  return 'create_user: ok'
