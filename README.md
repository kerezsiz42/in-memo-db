# In Memo Database

### Resources

https://12factor.net/
https://docs.python.org/3/library/hashlib.html#hashlib.pbkdf2_hmac
https://docs.python.org/3/library/pickle.html
https://docs.python.org/3/library/asyncio-stream.html
https://stackoverflow.com/questions/42040134/execute-function-based-on-functions-name-string

### Features

- in memory database
- persistence on disk
- single threaded, concurrent working
- asyncio
- 12 factor principle (env variables)
- key value store
- multiple distinct db
- safe user and resorce handling with authorization and authentication
- custom communication protocol using tcp sockets
- no burnt in constant

### TODO:

- ttl
- delete_user, delete_db
- pickle
- fast partial save
- tidy things up
- tests
- documentation
