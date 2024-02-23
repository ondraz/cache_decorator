
PYTHON_PATH=""
.PHONY: install install_test test build publish pytest publish_codeartifact

install:
	$(PYTHON_PATH)pip install --upgrade .

install_test:
	$(PYTHON_PATH)pip install --upgrade ".[test]"

test:
	$(PYTHON_PATH)pytest -s --cov cache_decorator --cov-report html

build:
	$(PYTHON_PATH)python setup.py sdist

publish:
	$(PYTHON_PATH)twine upload "./dist/$$(ls ./dist | grep .tar.gz | sort | tail -n 1)"

pytest:
	rm -rfd test_cache
	pytest -s
	rm -rfd test_cache

publish_codeartifact: build
	aws codeartifact login --tool twine --repository upheal --domain upheal --domain-owner 746959089469 --region eu-central-1
	twine upload --repository codeartifact ./dist/*
