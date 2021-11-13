# This codebase has been developed on Linux with Python version 3.8.10 64-bit
start:
	python3 main.py
start-container:
	docker compose up --build in-memo-db
test:
	python3 -m unittest -v
manual-test:
	nc localhost 8888
clean:
	rm -rf state_files/*
	echo "This folder has to be present in the folder structure, because the state is saved here." > state_files/README.md
