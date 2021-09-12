# import pickle
import asyncio
import os
import signal
import logging
import sys

# Dotenv should be the first custom module to import
import dotenv
from handler import handler

logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', stream=sys.stdout,level=logging.INFO)

async def main_coro():
  try:
    server = await asyncio.start_server(handler, os.environ['HOST'], os.environ['PORT'])
    addr = server.sockets[0].getsockname()
    logging.info(f'serving on {addr[0]}:{addr[1]}')
    await server.start_serving()
    await asyncio.Event().wait()
  except asyncio.CancelledError:
    server.close()
    await server.wait_closed()
    logging.info('graceful shutdown: ok')

if __name__ == '__main__':
  logging.info(f'pid: {os.getpid()}')
  loop = asyncio.get_event_loop()
  main_task = asyncio.ensure_future(main_coro())
  loop.add_signal_handler(signal.SIGTERM, main_task.cancel)
  loop.add_signal_handler(signal.SIGINT, main_task.cancel)
  loop.run_until_complete(main_task)