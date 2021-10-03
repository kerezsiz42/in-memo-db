# This codebase is compatible with python 3.8.10

start:
	python3 main.py
start-container:
	sudo docker compose up --build in-memo-db
test:
	python3 -m unittest -v
manual-test:
	nc localhost 8888

# e2e-test

# load-test