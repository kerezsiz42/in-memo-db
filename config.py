import os
import dotenv

dotenv.load_config()

# Each of os.environ[] would throw a KeyError if their envvar is unset
ROOT_USER = os.environ['ROOT_USER']
ROOT_PASSWORD = os.environ['ROOT_PASSWORD']

PORT = os.environ['PORT']
HOST = os.environ['HOST']

PBKDF2_HMAC_ITERATIONS = int(os.environ['PBKDF2_HMAC_ITERATIONS'])
