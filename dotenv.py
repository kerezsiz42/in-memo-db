import os

FILENAME = '.env'


def load_config(filename=FILENAME):
  """Loads variables from the specified .env file and sets them as environment vars if they are not set already."""
  try:
    with open(filename, 'r', encoding='UTF-8') as file:
      lines = file.readlines()
      for line in lines:
        if line[0] == '#':
          continue
        stripped_line = line.rstrip()
        if stripped_line == '':
          continue
        envvar_name, envvar_value = stripped_line.split('=')
        if envvar_name not in os.environ:
          os.environ[envvar_name] = envvar_value
  # EAFP principle: https://docs.python.org/3/glossary.html
  except FileNotFoundError:
    pass
