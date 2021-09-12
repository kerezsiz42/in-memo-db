import os

FILENAME = '.env'

with open(FILENAME, 'r', encoding='UTF-8') as file:
  lines = file.readlines()
  for line in lines:
    if line[0] == '#':
      continue
    stripped_line = line.rstrip()
    if len(stripped_line) == 0:
      continue
    name_value_pair = stripped_line.split('=')
    envvar_name = name_value_pair[0]
    envvar_value = name_value_pair[1]
    if envvar_name not in os.environ:
      os.environ[envvar_name] = envvar_value
