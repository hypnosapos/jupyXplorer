#!/bin/sh
DIR=$(dirname "$0")

cd ${DIR}

test() {

    pytest --cov=jupyxplorer --cov-report term-missing --cov-fail-under 80 --pep8

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
        echo "Usage: $0 {test|codecov|build|publish}"
        exit 1
esac