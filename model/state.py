import logging
import pickle
import os
from config import ROOT_PASSWORD, ROOT_USER
from model.store import Store


STATE_FILES_DIRNAME = 'state_files'
STORE_FILENAME = f'{STATE_FILES_DIRNAME}/store.pickle'
SEQUENTIAL_SAVE_FILENAME = f'{STATE_FILES_DIRNAME}/sequential_save.txt'


class State:
  @staticmethod
  def load_sequential_save_file() -> None:
    try:
      with open(SEQUENTIAL_SAVE_FILENAME, 'r') as file:
        for line in file:
          print(line, end='')
      logging.info(f'loaded {SEQUENTIAL_SAVE_FILENAME}')
    except FileNotFoundError:
      pass
    else:
      State.delete_sequential_save_file()

  @staticmethod
  def delete_sequential_save_file() -> None:
    try:
      os.remove(SEQUENTIAL_SAVE_FILENAME)
      logging.info(f'deleted {SEQUENTIAL_SAVE_FILENAME}')
    except OSError:
      pass

  @staticmethod
  def load_store_from_disk() -> Store:
    try:
      with open(STORE_FILENAME, 'rb') as file:
        store = pickle.load(file=file)
        logging.info(f'state loaded from {STORE_FILENAME}')
    except FileNotFoundError:
      logging.info('no savefile found')
      store = Store()
      store.create_user(ROOT_USER, ROOT_PASSWORD)
      logging.info('registered root user from env vars')
    finally:
      State.load_sequential_save_file()
      return store

  @staticmethod
  def save_store_to_disk(store: Store) -> None:
    with open(STORE_FILENAME, 'wb') as file:
      pickle.dump(store, file=file)
      logging.info(f'state saved in {STORE_FILENAME}')
    State.delete_sequential_save_file()

  @staticmethod
  def append_successful_command(line: str) -> None:
    with open(SEQUENTIAL_SAVE_FILENAME, 'a') as file:
      file.write(line + '\n')
