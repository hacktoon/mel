PYTHON_DEBUGGER=ipdb.set_trace

install:
	cp bin/pre-commit.sh .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit
	chmod +x bin/mel
	pip install --upgrade pip
	pip install -r requirements.txt

install-dev:
	pip install ipython ipdb

upgrade:
	pip install --upgrade pip -r requirements.txt

lint:
	flake8 .

clean:
	find . -name '__pycache__' -exec rm -rf {} +

test:
	pytest --color=yes --cov --durations=3 --no-cov-on-fail -vv

debug:
ifdef TEST
	PYTHONBREAKPOINT=$(PYTHON_DEBUGGER) pytest -sk $(TEST)
else
	PYTHONBREAKPOINT=$(PYTHON_DEBUGGER) pytest -s
endif

docker-build:
	docker build -t mel .

python-watch:
	@ack -f --python | entr make test