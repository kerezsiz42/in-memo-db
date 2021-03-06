class CustomException(Exception):
  pass


DbNotExistError = CustomException('database does not exist')
InvalidCommandError = CustomException('invalid command')
UsernameAlreadyTakenError = CustomException('username already taken')
UserNotExistError = CustomException('user does not exist')
DbAlreadyExistsError = CustomException('database already exist with the same name')
InvalidKeyError = CustomException('invalid key')
InvalidNumberOfParamsError = CustomException('invalid number of parameters')
InvalidCredentialsError = CustomException('invalid credentials')
UserNotLoggedInError = CustomException('you must be logged in')
NoDbSelectedError = CustomException('no database selected')
UserUnauthorizedError = CustomException('only root user can do this action')
InvalidTTLValueError = CustomException('invalid ttl: should be integer')
CannotDeleteRootUserError = CustomException('cannot delete root user')
