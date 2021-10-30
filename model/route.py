from enum import Enum, unique


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
