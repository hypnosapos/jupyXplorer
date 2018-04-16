#!/bin/sh
DIR=$(dirname "$0")

cd ${DIR}

test() {

    pytest --cov=jupyxplorer --pep8

}

codecov() {

    codecov;

}

build() {

    python setup.py sdist bdist_wheel

}

publish() {

    echo;

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
        codecov "$@"
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