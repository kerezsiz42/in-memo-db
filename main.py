# import pickle
import asyncio
import os
import signal
import logging
import sys

from config import HOST, PORT, ROOT_PASSWORD, ROOT_USER
from handlers import create_db, register_user, current_db, delete, delete_db, delete_user, get, list_dbs, list_users, login, put, select_db, update, whoami
from model.router import Router
from model.store import Store


async def main_coro():
  try:
    store = Store()
    # Load saved store data here
    store.create_user(ROOT_USER, ROOT_PASSWORD)
    router = Router()
    router.use('login', [login])
    router.use('whoami', [whoami])
    router.use('register_user', [register_user])
    router.use('create_db', [whoami, create_db])
    router.use('select_db', [whoami, select_db])
    router.use('delete_db', [whoami, delete_db])
    router.use('delete_user', [whoami, delete_user])
    router.use('list_users', [whoami, list_users])
    router.use('list_dbs', [whoami, list_dbs])
    router.use('current_db', [whoami, current_db])
    router.use('get', [whoami, current_db, get])
    router.use('put', [whoami, current_db, put])
    router.use('delete', [whoami, current_db, delete])
    router.use('update', [whoami, current_db, update])
    server = await asyncio.start_server(lambda r, w: router(r, w, store), host=HOST, port=PORT)
    host, port = server.sockets[0].getsockname()
    logging.info(f'serving on {host}:{port}')
    await server.start_serving()
    # Other server wide tasks come here
    await asyncio.Event().wait()
  except asyncio.CancelledError:
    server.close()
    await server.wait_closed()
    # Save store data here
    logging.info('graceful shutdown: ok')

if __name__ == '__main__':
  logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', stream=sys.stdout, level=logging.INFO)
  logging.info(f'pid: {os.getpid()}')
  loop = asyncio.get_event_loop()
  main_task = loop.create_task(main_coro())
  loop.add_signal_handler(signal.SIGTERM, main_task.cancel)
  loop.add_signal_handler(signal.SIGINT, main_task.cancel)
  loop.run_until_complete(main_task)
