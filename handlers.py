from config import ROOT_USER
from model.database import Key, Value
from model.exception import InvalidCredentialsError, InvalidNumberOfParamsError, NoDbSelectedError, UserNotLoggedInError, UserUnauthorizedError
from model.router import Context
from model.store import DatabaseName, Username


def login(ctx: Context) -> str:
  try:
    username: Username = ctx.params[0]
    password: str = ctx.params[1]
  except IndexError:
    raise InvalidNumberOfParamsError
  if len(username) == 0 or len(password) == 0 or not ctx.store.authenticate_user(username, password):
    raise InvalidCredentialsError
  ctx.username = username
  ctx.database_name = str()
  ctx.database = None
  return 'login: ok'


def whoami(ctx: Context) -> Username:
  username = ctx.username
  if len(username) == 0:
    raise UserNotLoggedInError
  return username


def create_db(ctx: Context) -> str:
  try:
    new_db_name: DatabaseName = ctx.params[0]
  except IndexError:
    raise InvalidNumberOfParamsError
  username = ctx.username
  ctx.store.create_database(username=username, new_db_name=new_db_name)
  ctx.store.add_user_to_owners(username=ROOT_USER, db_name=new_db_name)
  return 'create_db: ok'


def select_db(ctx: Context) -> str:
  try:
    db_name: DatabaseName = ctx.params[0]
  except IndexError:
    raise InvalidNumberOfParamsError
  ctx.database = ctx.store.get_database_by_name(username=ctx.username, db_name=db_name)
  ctx.database_name = db_name
  return 'select_db: ok'


def current_db(ctx: Context) -> DatabaseName:
  if len(ctx.database_name) == 0:
    raise NoDbSelectedError
  return ctx.database_name


def get(ctx: Context) -> Value:
  try:
    key: Key = ctx.params[0]
  except IndexError:
    raise InvalidNumberOfParamsError
  return ctx.database.get(key=key)


def put(ctx: Context) -> str:
  try:
    key: Key = ctx.params[0]
    value: Value = ctx.params[1]
  except IndexError:
    raise InvalidNumberOfParamsError
  ctx.database.put(key=key, value=value)
  return 'put: ok'


def delete(ctx: Context) -> str:
  try:
    key: Key = ctx.params[0]
  except IndexError:
    raise InvalidNumberOfParamsError
  ctx.database.delete(key=key)
  return 'delete: ok'


def update(ctx: Context) -> str:
  try:
    key: Key = ctx.params[0]
    value: Value = ctx.params[1]
  except IndexError:
    raise InvalidNumberOfParamsError
  ctx.database.update(key=key, value=value)
  return 'update: ok'


def delete_user(ctx: Context) -> str:
  if ctx.username != ROOT_USER:
    raise UserUnauthorizedError
  try:
    user_to_delete: Username = ctx.params[0]
  except IndexError:
    raise InvalidNumberOfParamsError
  ctx.store.delete_user(user_to_delete=user_to_delete)
  return 'delete_user: ok'


def delete_db(ctx: Context) -> str:
  try:
    db_to_delete: DatabaseName = ctx.params[0]
  except IndexError:
    raise InvalidNumberOfParamsError
  ctx.store.delete_database(username=ctx.username, db_to_delete=db_to_delete)
  current_selected_db_name = ctx.database_name
  if current_selected_db_name == db_to_delete:
    ctx.database_name = str()
  return 'delete_db: ok'


def list_users(ctx: Context) -> str:
  set_of_users = ctx.store.list_users_of_db(db_name=ctx.database_name)
  return str(list(set_of_users))


def list_dbs(ctx: Context) -> str:
  set_of_dbs = ctx.store.list_dbs_of_user(username=ctx.username)
  return str(list(set_of_dbs))


def register_user(ctx: Context) -> str:
  try:
    username_to_create: Username = ctx.params[0]
    password: str = ctx.params[1]
  except IndexError:
    raise InvalidNumberOfParamsError
  ctx.store.create_user(username_to_create=username_to_create, password=password)
  return 'create_user: ok'
