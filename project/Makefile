VENV := .venv
PIP := $(VENV)/bin/pip
PIPENV := $(VENV)/bin/pipenv

export PIPENV_VENV_IN_PROJECT=1
export PIPENV_VERBOSITY=-1
export PYTHONPATH=.

activate_venv: $(VENV)/bin/activate

env:
	python3 -m virtualenv $(VENV)

clean-env:
	rm -rf $(VENV)

clean:
	rm -rfv .pytest_cache __pycache__/ tests/__pycache__ htmlcov htmltest .coverage

install: env activate_venv
	$(PIP) install pipenv
	$(PIPENV) install

install-dev: install
	$(PIPENV) install --dev

lint: install-dev
	$(PIPENV) run black . --diff
	$(PIPENV) run flake8

lint-apply: install-dev
	$(PIPENV) run black .