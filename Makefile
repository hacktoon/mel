PYTHON_DEBUGGER=pudb.set_trace

install:
ifdef DEV
	pip install ipython pudb
endif
	cp bin/pre-commit.sh .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit
	chmod +x bin/dale
	pip install --upgrade pip
	pip install -r requirements.txt

upgrade:
	pip install --upgrade pip -r requirements.txt

inspect:
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
