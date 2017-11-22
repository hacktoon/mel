test:
	pytest --color=yes --cov --durations=3 --no-cov-on-fail --cov-config=settings/.coveragerc

debug:
	pytest -s