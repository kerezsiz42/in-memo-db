# In Memo Database

### Resources

https://12factor.net/
https://docs.python.org/3/library/hashlib.html#hashlib.pbkdf2_hmac
https://docs.python.org/3/library/pickle.html
https://docs.python.org/3/library/asyncio-stream.html
https://docs.python.org/3/library/unittest.html
https://redis.io/commands
- koa & express js patterns

### Features

- in memory database
  - multiple distinct db
  - key value store
- persistence on disk, pickle
- single threaded
- concurrent, asyncio
- 12 factor principles
  - configurable by environment variables
- safe user and resource handling with authorization and authentication
- database creation, listing and deletion
- custom communication protocol using tcp sockets

### TODO:

- ttl
- pickle
- fast partial save
- tests
- documentation
