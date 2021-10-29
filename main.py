#!/usr/bin/python3.8
import asyncio
import os
import signal
import logging
import sys
from config import HOST, PORT
from model.router import Router
from model.store import Store


async def ttl_coro(store: Store) -> None:
  while True:
    await asyncio.sleep(delay=1.0)
    store.delete_expired_keys_from_dbs()


async def main_coro() -> None:
  try:
    store = Store()
    store.load_dbs_from_disk()
    router = Router(store=store)
    router.load_sequential_save_file()
    server = await asyncio.start_server(router, host=HOST, port=PORT)
    logging.info(f'serving on {HOST}:{PORT}')
    asyncio.create_task(ttl_coro(store=store))
    await server.start_serving()
    await asyncio.Event().wait()
  except asyncio.CancelledError:
    server.close()
    await server.wait_closed()
    store.save_dbs_to_disk()
    router.delete_sequential_save_file()
    logging.info('graceful shutdown: ok')

if __name__ == '__main__':
  logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', stream=sys.stdout, level=logging.INFO)
  logging.info(f'pid: {os.getpid()}')
  loop = asyncio.get_event_loop()
  main_task = loop.create_task(main_coro())
  loop.add_signal_handler(signal.SIGTERM, main_task.cancel)
  loop.add_signal_handler(signal.SIGINT, main_task.cancel)
  loop.run_until_complete(main_task)
