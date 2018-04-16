.PHONY: help clean clean-build clean-pyc clean-test test build install release codecov doc
.DEFAULT_GOAL := help

DOCKER_ORG        ?= hypnosapos
DOCKER_IMAGE      ?= jupyxplorer
DOCKER_USERNAME   ?= letigo
DOCKER_PASSWORD   ?= topsecret
PY_ENVS           ?= 3.5 3.6
DEFAULT_PY_ENV    ?= 3.5


help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


clean-build: ## remove build artifacts
	rm -rf build dist .eggs .cache docs/build
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -rf .tox .coverage htmlcov coverage-reports

build-test-images: ## Build nested docker images for testing porpouses
	@ $(foreach py_env,\
		$(PY_ENVS),\
		docker build --build-arg PY_VERSION=$(py_env) -t $(DOCKER_ORG):jupyxplorer-py$(py_env)-test -f Dockerfile.test .;)

test: build-test-images ## run tests, based on docker
	@ $(foreach py_env,$(PY_ENVS),docker run $(DOCKER_ORG):jupyxplorer-py$(py_env)-test ./entry.sh test;)

build: ## build the wheel :)
	@tox -e build

install: ## install jupyXplorer
	pip install .

develop: ## develop jupyXplorer
	pip install --editable .

release: ## upload release to pypi
	@tox -e release

codecov: ## update coverage to codecov
	@tox -e codecov

doc: ## create documentation
	@tox -e doc
