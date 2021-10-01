# import pickle
import asyncio
import os
import signal
import logging
import sys

from config import HOST, PORT, ROOT_PASSWORD, ROOT_USER
from handler import handler
from model.store import Store


async def main_coro():
  try:
    store = Store()
    # Load saved state here
    store.create_user(ROOT_USER, ROOT_PASSWORD)
    server = await asyncio.start_server(lambda reader, writer: handler(reader, writer, store), host=HOST, port=PORT)
    host, port = server.sockets[0].getsockname()
    logging.info(f'serving on {host}:{port}')
    await server.start_serving()
    # Other server wide tasks come here
    await asyncio.Event().wait()
  except asyncio.CancelledError:
    server.close()
    await server.wait_closed()
    # Save state here
    logging.info('graceful shutdown: ok')

if __name__ == '__main__':
  logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', stream=sys.stdout, level=logging.INFO)
  logging.info(f'pid: {os.getpid()}')
  loop = asyncio.get_event_loop()
  main_task = asyncio.ensure_future(main_coro())
  loop.add_signal_handler(signal.SIGTERM, main_task.cancel)
  loop.add_signal_handler(signal.SIGINT, main_task.cancel)
  loop.run_until_complete(main_task)
