#--------------------------------------------------
# Local development with pyenv (to use with your IDE)

PY_VERSION=3.10.0
PYENV_NAME=viooh_activity
PYENV=~/.pyenv/versions/${PY_VERSION}/envs/${PYENV_NAME}/bin

install:
	pip install -r requirements.txt

freeze: requirements

docker-build-dev:
	docker build -t audience-performance-reporting . --build-arg REQUIREMENTS_SUFFIX=-dev

docker-run-dev:
	docker run -it audience-performance-reporting /bin/bash

test:
	python -m pytest -sv tests/unit/
