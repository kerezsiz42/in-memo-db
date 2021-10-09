# In Memo Database

### Overview

The goal of this development is to create an in-memory cache that can be used by http servers
and other services and is faster at retrieving and setting data than conventional databases.
It stores data in RAM and provides an simple interface for clients to access their data through
a custom protocol built on top of TCP sockets.

### Features

- 12 factor app principles
  - [x] codebase tracked in version control
  - [x] no dependencies (no libraries, only built in functions)
  - [x] configurable by environment variables
  - [x] no backing services
  - [x] containerized (build stage)
  - [x] app runs as a singular process (no replica set behavior implemented yet)
  - [x] service exported via port binding
  - [x] runs as a UNIX process
  - [x] graceful shutdown on SIGTERM or SIGINT
  - [ ] no production environment yet
  - [x] logs out to stout
  - [ ] no admin processes
- multiple distinct db
- safe user and resource handling with authorization and authentication
  - users are able to create, list and delete their databases
- single threaded, concurrent working, using the build-in asyncio library
- key expiration can be set (i.e. for expiring sessions)

### TODO:

- persistence on disk using the pickle library
- fast sequential save (?)
- tests
- documentation

### Resources

https://12factor.net/
https://docs.python.org/3/library/hashlib.html#hashlib.pbkdf2_hmac
https://docs.python.org/3/library/pickle.html
https://docs.python.org/3/library/asyncio-stream.html
https://docs.python.org/3/library/unittest.html
https://redis.io/commands
- koa & express js patterns