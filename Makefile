all: lint

REBUILD_FLAG=

.PHONY: lint
lint:
	flake8 --ignore=E501,W503

.venv/touch: Makefile
	python3 -m venv .venv
	set -e ; . .venv/bin/activate ; pip install --upgrade pip ; pip install --upgrade setuptools ; pip install tox ; pip install build
	touch .venv/touch

.PHONY: venv
venv: .venv/touch

.tox/touch: requirements.txt requirements_dev.txt
	$(eval REBUILD_FLAG := --recreate)
	touch .tox/touch

test: venv .tox/touch
	. .venv/bin/activate ; tox $(REBUILD_FLAG)

.PHONY: release
release:
	. .venv/bin/activate ; python3 -m build
	. .venv/bin/activate ; python3 -m twine upload dist/*

.PHONY: clean
clean:
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete
	rm -rf build
	rm -rf dist
	rm -rf src/*.egg-info
