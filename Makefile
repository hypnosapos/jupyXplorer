.PHONY: help clean test test-e2e build release codecov venv
.DEFAULT_GOAL := help

DOCKER_ORG       ?= hypnosapos
DOCKER_IMAGE     ?= jupyxplorer
DOCKER_USERNAME  ?= letigo
DOCKER_PASSWORD  ?= topsecret
DOCKER_TAG       ?= latest
PY_ENVS          ?= 3.5 3.6
DEFAULT_PY_ENV   ?= 3.5


help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean-build:
	rm -rf build dist .eggs .cache docs/build .output tests/.output-test
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +
	docker rm -f $$(docker ps -a -f "ancestor=$(DOCKER_ORG)/jupyxplorer:$(DOCKER_TAG)" --format '{{.Names}}') > /dev/null 2>&1 || echo "No containers"
	docker rmi -f $(DOCKER_ORG)/jupyxplorer:$(DOCKER_TAG)
	$(foreach py_env,\
	  $(PY_ENVS),\
	  docker rm -f $$(docker ps -a -f "ancestor=$(DOCKER_ORG)/jupyxplorer-py$(py_env)-test" --format '{{.Names}}') > /dev/null 2>&1 || echo "No containers";\
	  docker rmi -f $(DOCKER_ORG)/jupyxplorer-py$(py_env)-test;)

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-env:
	rm -rf .venv

clean: clean-build clean-pyc clean-env ## Remove all built resources, test, coverage, and other output files

build-test-images:
	@ $(foreach py_env,\
		$(PY_ENVS),\
		docker build --build-arg PY_VERSION=$(py_env) -t $(DOCKER_ORG)/jupyxplorer-py$(py_env)-test -f Dockerfile.test .;)

test: build-test-images ## Run tests, based on docker
	@ $(foreach py_env,$(PY_ENVS),docker run -ti $(DOCKER_ORG)/jupyxplorer-py$(py_env)-test ./entry.sh test;)

test_e2e: ## End2End tests
	@docker-compose -f tests/e2e/docker-compose.yaml up --exit-code-from jupyxplorer --build
	@docker-compose -f tests/e2e/docker-compose.yaml down

build: ## Build the docker image
	@docker build -t $(DOCKER_ORG)/jupyxplorer:$(DOCKER_TAG) .

default-build:
	@docker build --build-arg PY_VERSION=$(DEFAULT_PY_ENV) -t $(DOCKER_ORG)/jupyxplorer-py$(DEFAULT_PY_ENV)-test -f Dockerfile.test .

release: default-build ## Upload release to pypi
	@docker run -ti $(DOCKER_ORG)/jupyxplorer-py$(DEFAULT_PY_ENV)-test bash -c "./entry.sh build && ./entry.sh publish"

codecov: default-build ## Update coverage to codecov
	@docker run -ti $(DOCKER_ORG)/jupyxplorer-py$(DEFAULT_PY_ENV)-test bash -c "./entry.sh test && ./entry.sh codecov"

venv: ## Create a local virtualenv with default python version (supported 3.5 and 3.6)
	python -m venv .venv
	source .venv/bin/activate && pip install -U pip && pip install -r requirements.txt -r requirements-dev.txt
	echo "\033[32m[[ Type 'source .venv/bin/activate' to activate virtualenv ]]\033[0m"
