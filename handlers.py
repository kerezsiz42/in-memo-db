from config import ROOT_USER
from model.database import Key
from model.exception import CannotDeleteRootUserError, InvalidCredentialsError, InvalidNumberOfParamsError, InvalidTTLValueError, NoDbSelectedError, UserNotLoggedInError, UserUnauthorizedError
from model.router import Context


def login(ctx: Context) -> None:
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
  ctx.response = 'login: ok'


def whoami(ctx: Context) -> None:
  if ctx.username == '':
    raise UserNotLoggedInError
  ctx.response = ctx.username


def create_db(ctx: Context) -> None:
  try:
    new_db_name = ctx.params[0]
  except IndexError:
    raise InvalidNumberOfParamsError
  ctx.store.create_database(username=ctx.username, new_db_name=new_db_name)
  ctx.store.add_user_to_owners(username=ROOT_USER, db_name=new_db_name)
  ctx.response = 'create_db: ok'


def add_user_to_owners(ctx: Context) -> None:
  try:
    new_owner_username = ctx.params[0]
    db_name = ctx.params[1]
  except IndexError:
    raise InvalidNumberOfParamsError
  if ctx.username != ROOT_USER:
    raise UserUnauthorizedError
  ctx.store.add_user_to_owners(username=new_owner_username, db_name=db_name)
  ctx.response = 'add_user_to_owners: ok'


def select_db(ctx: Context) -> None:
  try:
    db_name = ctx.params[0]
  except IndexError:
    raise InvalidNumberOfParamsError
  ctx.database = ctx.store.get_database_by_name(username=ctx.username, db_name=db_name)
  ctx.database_name = db_name
  ctx.response = 'select_db: ok'


def current_db(ctx: Context) -> None:
  if ctx.database_name == '':
    raise NoDbSelectedError
  ctx.response = ctx.database_name


def get(ctx: Context) -> None:
  try:
    key = ctx.params[0]
  except IndexError:
    raise InvalidNumberOfParamsError
  ctx.response = ctx.database.get(key=key)


def put(ctx: Context) -> None:
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
  ctx.response = 'put: ok'


def delete(ctx: Context) -> None:
  try:
    key: Key = ctx.params[0]
  except IndexError:
    raise InvalidNumberOfParamsError
  ctx.database.delete(key=key)
  ctx.response = 'delete: ok'


def update(ctx: Context) -> None:
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
  ctx.response = 'update: ok'


def delete_user(ctx: Context) -> None:
  if ctx.username != ROOT_USER:
    raise UserUnauthorizedError
  try:
    user_to_delete = ctx.params[0]
  except IndexError:
    raise InvalidNumberOfParamsError
  if user_to_delete == ROOT_USER:
    raise CannotDeleteRootUserError
  ctx.store.delete_user(user_to_delete=user_to_delete)
  ctx.response = 'delete_user: ok'


def delete_db(ctx: Context) -> None:
  try:
    db_to_delete = ctx.params[0]
  except IndexError:
    raise InvalidNumberOfParamsError
  ctx.store.delete_database(username=ctx.username, db_to_delete=db_to_delete)
  current_selected_db_name = ctx.database_name
  if current_selected_db_name == db_to_delete:
    ctx.database_name = str()
    ctx.database = None
  ctx.response = 'delete_db: ok'


def list_users(ctx: Context) -> None:
  ctx.response = str(ctx.store.list_users_of_db(db_name=ctx.database_name))


def list_dbs(ctx: Context) -> None:
  ctx.response = str(ctx.store.list_dbs_of_user(username=ctx.username))


def register_user(ctx: Context) -> None:
  try:
    username_to_create = ctx.params[0]
    password = ctx.params[1]
  except IndexError:
    raise InvalidNumberOfParamsError
  ctx.store.create_user(username_to_create=username_to_create, password=password)
  ctx.response = 'create_user: ok'
