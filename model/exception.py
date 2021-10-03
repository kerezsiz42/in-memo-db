class BaseException(Exception):
  def __init__(self, message: str = ''):
    self.message = message
    super().__init__(self.message)

  def __str__(self):
    return str(self.message)


DbNotExistError = BaseException('database does not exist')
InvalidCommandError = BaseException('invalid command')
UsernameAlreadyTakenError = BaseException('username already taken')
UserNotExistError = BaseException('user does not exist')
DbAlreadyExistsError = BaseException('database already exist with the same name')
InvalidKeyError = BaseException('invalid key')
InvalidNumberOfParamsError = BaseException('invalid number of parameters')
InvalidCredentialsError = BaseException('invalid credentials')
UserNotLoggedInError = BaseException('you must be logged in')
NoDbSelectedError = BaseException('no database selected')
UserUnauthorizedError = BaseException('only root user can delete users')
