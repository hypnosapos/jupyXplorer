.PHONY: help clean test test-e2e build install release codecov
.DEFAULT_GOAL := help

DOCKER_ORG       ?= hypnosapos
DOCKER_IMAGE      ?= jupyxplorer
DOCKER_USERNAME   ?= letigo
DOCKER_PASSWORD   ?= topsecret
DOCKER_TAG       ?= latest
PY_ENVS          ?= 3.5 3.6
DEFAULT_PY_ENV    ?= 3.5


help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean: clean-build clean-pyc ## remove all build, test, coverage, output files and Python artifacts

clean-build: ## remove build artifacts
	rm -rf build dist .eggs .cache docs/build .output .coverage htmlcov coverage-reports
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +
	docker rmi -f $(DOCKER_ORG)/jupyxplorer:$(DOCKER_TAG)

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

build-test-images: ## Build nested docker images for testing porpouses
	@ $(foreach py_env,\
		$(PY_ENVS),\
		docker build --build-arg PY_VERSION=$(py_env) -t $(DOCKER_ORG)/jupyxplorer-py$(py_env)-test -f Dockerfile.test .;)

test: build-test-images ## run tests, based on docker
	@ $(foreach py_env,$(PY_ENVS),docker run -ti $(DOCKER_ORG)/jupyxplorer-py$(py_env)-test ./entry.sh test;)

test-e2e: ## End2End tests
	@docker-compose -f tests/e2e/docker-compose.yaml up --exit-code-from jupyxplorer --build
	@docker-compose -f tests/e2e/docker-compose.yaml down

build: ## build the docker image
	@docker build -t $(DOCKER_ORG)/jupyxplorer:$(DOCKER_TAG) .

install: ## install jupyXplorer
	pip install .

develop: ## develop jupyXplorer
	pip install -e .

default-build:
	@docker build --build-arg PY_VERSION=$(DEFAULT_PY_ENV) -t $(DOCKER_ORG)/jupyxplorer-py$(DEFAULT_PY_ENV)-test -f Dockerfile.test .

release: default-build ## upload release to pypi
	@docker run -ti $(DOCKER_ORG)/jupyxplorer-py$(DEFAULT_PY_ENV)-test bash -c "./entry.sh build && ./entry.sh publish"

codecov: default-build ## update coverage to codecov
	@docker run -ti $(DOCKER_ORG)/jupyxplorer-py$(DEFAULT_PY_ENV)-test ./entry.sh codecov
