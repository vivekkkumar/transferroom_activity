#--------------------------------------------------
# Local development with pyenv (to use with your IDE)

PY_VERSION=3.10.0
PYENV_NAME=transferrom_activity
PYENV=~/.pyenv/versions/${PY_VERSION}/envs/${PYENV_NAME}/bin

install:
	pip install -r requirements.txt

freeze: requirements

docker-build-dev:
	docker build -t reporting-app . --build-arg REQUIREMENTS_SUFFIX=-dev

docker-run-dev:
	docker run -it reporting /bin/bash

test:
	python -m pytest -sv tests/unit/
