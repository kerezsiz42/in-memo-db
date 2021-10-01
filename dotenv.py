import os

FILENAME = '.env'


def load_config(filename=FILENAME):
  try:
    with open(filename, 'r', encoding='UTF-8') as file:
      lines = file.readlines()
      for line in lines:
        if line[0] == '#':
          continue
        stripped_line = line.rstrip()
        if len(stripped_line) == 0:
          continue
        envvar_name, envvar_value = stripped_line.split('=')
        if envvar_name not in os.environ:
          os.environ[envvar_name] = envvar_value
  except FileNotFoundError:
    pass
