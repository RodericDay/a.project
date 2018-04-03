include .env
export

default: jsbuild test

run:
	cd server && venv/bin/gunicorn src.api:app

rundev: server/venv
	cd server && venv/bin/python src/api.py

jsbuild: client/node_modules
	cd client && tsc

test: server/venv
	cd server && venv/bin/py.test src tests --doctest-modules --failed-first -vv
	cd server && venv/bin/flake8 src tests

server/venv: server/requirements.txt
	cd server && rm -rf venv
	cd server && python3 -m venv venv
	cd server && venv/bin/pip install -r requirements.txt

client/node_modules: client/package.json
	cd client && rm -rf node_modules
	cd client && npm install

deploy: test
	git status --porcelain
	# nginx
	# gunicorn
	# rsync

backup:

clean:
	git clean -dxn
