install:
	pip install -r requirements.txt
	
install-dev:
	pip install ipython ipdb

upgrade:
	pip install --upgrade pip -r requirements.txt

inspect:
	flake8 .

test:
	pytest --color=yes --cov --durations=3 --no-cov-on-fail -v

debug:
	pytest -s

