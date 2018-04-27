#!/bin/sh -e
DIR=$(dirname "$0")

cd ${DIR}

test() {

    pytest --cov=jupyxplorer --cov-report term-missing --cov-fail-under 80 --pep8

}

test_e2e() {

    pip install -e .
    jupyxplorer -c ${DIR}/tests/e2e/sample_config.yaml
    cmp --silent ${DIR}/tests/e2e/exploration_cat_species.ipynb ${DIR}/.output/exploration_cat_species.ipynb
    cmp --silent ${DIR}/tests/e2e/exploration_num_petalLength.ipynb ${DIR}/.output/exploration_num_petalLength.ipynb
    cmp --silent ${DIR}/tests/e2e/exploration_num_sepalLength.ipynb ${DIR}/.output/exploration_num_sepalLength.ipynb

}

_codecov() {

    codecov

}

build() {

    python setup.py sdist bdist_wheel

}

publish() {

    twine upload --skip-existing dist/*

}


# Main options
case "$1" in
  test)
        shift
        test "$@"
        exit $?
        ;;
  test_e2e)
        shift
        test_e2e "$@"
        exit $?
        ;;
  codecov)
        shift
        _codecov "$@"
        exit $?
        ;;
  build)
        shift
        build "$@"
        exit $?
        ;;
  publish)
        shift
        publish "$@"
        exit $?
        ;;
  *)
        echo "Usage: $0 {test|test_e2e|codecov|build|publish}"
        exit 1
esac