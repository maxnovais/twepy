SHELL=/bin/bash

clean:
	@find . -iname '*.py[co]' -delete
	@find . -name '__pycache__' -prune | xargs rm -rf # clean __pycache__ dirs build by py.test

deps:
	pip install -r requirements.txt
	cp app/config.py.example app/config.py

up:
	sudo docker-compose up -d

stop:
	sudo docker-compose stop

auth:
	python app/twitter-authorize.py

stream:
	python app/twitter-stream.py
