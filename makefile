# This codebase has benn developed on Linux Python version 3.8.10 64-bit
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