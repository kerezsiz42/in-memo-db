from config import ROOT_USER
from model.database import Key, Value
from model.exception import InvalidCredentialsError, InvalidNumberOfParamsError, InvalidTTLValueError, NoDbSelectedError, UserNotLoggedInError, UserUnauthorizedError
from model.router import Context
from model.store import DatabaseName, Username


def login(ctx: Context) -> str:
  try:
    username = ctx.params[0]
    password = ctx.params[1]
  except IndexError:
    raise InvalidNumberOfParamsError
  if not ctx.store.authenticate_user(username, password):
    raise InvalidCredentialsError
  ctx.username = username
  ctx.database_name = str()
  ctx.database = None
  return 'login: ok'


def whoami(ctx: Context) -> Username:
  if ctx.username == '':
    raise UserNotLoggedInError
  return ctx.username


def create_db(ctx: Context) -> str:
  try:
    new_db_name = ctx.params[0]
  except IndexError:
    raise InvalidNumberOfParamsError
  ctx.store.create_database(username=ctx.username, new_db_name=new_db_name)
  ctx.store.add_user_to_owners(username=ROOT_USER, db_name=new_db_name)
  return 'create_db: ok'


def add_user_to_owners(ctx: Context) -> str:
  try:
    new_owner_username = ctx.params[0]
    db_name = ctx.params[1]
  except IndexError:
    raise InvalidNumberOfParamsError
  if ctx.username != ROOT_USER:
    raise UserUnauthorizedError
  ctx.store.add_user_to_owners(username=new_owner_username, db_name=db_name)
  return 'add_user_to_owners: ok'


def select_db(ctx: Context) -> str:
  try:
    db_name = ctx.params[0]
  except IndexError:
    raise InvalidNumberOfParamsError
  ctx.database = ctx.store.get_database_by_name(username=ctx.username, db_name=db_name)
  ctx.database_name = db_name
  return 'select_db: ok'


def current_db(ctx: Context) -> DatabaseName:
  if ctx.database_name == '':
    raise NoDbSelectedError
  return ctx.database_name


def get(ctx: Context) -> Value:
  try:
    key = ctx.params[0]
  except IndexError:
    raise InvalidNumberOfParamsError
  return ctx.database.get(key=key)


def put(ctx: Context) -> str:
  try:
    key = ctx.params[0]
    value = ctx.params[1]
  except IndexError:
    raise InvalidNumberOfParamsError
  ctx.database.put(key=key, value=value)
  try:
    ttl_string = ctx.params[2]
  except IndexError:
    ctx.database.remove_ttl(key=key)
  else:
    if not ttl_string.isdigit():
      raise InvalidTTLValueError
    ttl = int(ttl_string)
    ctx.database.set_ttl(key=key, ttl=ttl)
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
    key = ctx.params[0]
    value = ctx.params[1]
  except IndexError:
    raise InvalidNumberOfParamsError
  ctx.database.update(key=key, value=value)
  try:
    ttl_string = ctx.params[2]
  except IndexError:
    ctx.database.remove_ttl(key=key)
  else:
    if not ttl_string.isdigit():
      raise InvalidTTLValueError
    ttl = int(ttl_string)
    ctx.database.set_ttl(key=key, ttl=ttl)
  return 'update: ok'


def delete_user(ctx: Context) -> str:
  if ctx.username != ROOT_USER:
    raise UserUnauthorizedError
  try:
    user_to_delete = ctx.params[0]
  except IndexError:
    raise InvalidNumberOfParamsError
  ctx.store.delete_user(user_to_delete=user_to_delete)
  return 'delete_user: ok'


def delete_db(ctx: Context) -> str:
  try:
    db_to_delete = ctx.params[0]
  except IndexError:
    raise InvalidNumberOfParamsError
  ctx.store.delete_database(username=ctx.username, db_to_delete=db_to_delete)
  current_selected_db_name = ctx.database_name
  if current_selected_db_name == db_to_delete:
    ctx.database_name = str()
  return 'delete_db: ok'


def list_users(ctx: Context) -> str:
  return str(ctx.store.list_users_of_db(db_name=ctx.database_name))


def list_dbs(ctx: Context) -> str:
  return str(ctx.store.list_dbs_of_user(username=ctx.username))


def register_user(ctx: Context) -> str:
  try:
    username_to_create = ctx.params[0]
    password = ctx.params[1]
  except IndexError:
    raise InvalidNumberOfParamsError
  ctx.store.create_user(username_to_create=username_to_create, password=password)
  return 'create_user: ok'
