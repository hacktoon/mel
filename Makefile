install-deps:
	pip install -r requirements.txt

upgrade-deps:
	pip install --upgrade pip -r requirements.txt

test:
	pytest --color=yes --cov --durations=3 --no-cov-on-fail

debug:
	pytest -s