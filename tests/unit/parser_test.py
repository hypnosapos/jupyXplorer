# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

import jupyxplorer.parser as parser

import pytest

from . import CONFIG_EXAMPLE


def test_load_yaml(mocker):
    # Given
    data = CONFIG_EXAMPLE
    file_path = "/path/tests"
    expected_result = data

    mocker.patch.object(parser.yaml, "load", return_value=expected_result)
    file_open_mock = mocker.patch("builtins.open")
    file_open_mock.read_data = data

    # When
    result = parser.load_yaml(file_path)

    file_open_mock.assert_called_once_with(file_path, 'r')

    # Then
    assert result == expected_result


def test_invalid_doc_error(mocker):

    data = "data"
    file_path = "/path/tests"

    mocker.patch.object(parser.yaml, "load", return_value=data)
    file_open_mock = mocker.patch("builtins.open")
    file_open_mock.read_data = data

    with pytest.raises(Exception, match=r'YAML SyntaxError:.*document.*'):
        parser.load_yaml(file_path)

    file_open_mock.assert_called_once_with(file_path, 'r')


def test_syntax_error(mocker):

    data = dict(
        manolo='esetioeh!'
    )
    file_path = "/path/tests"
    expected_line = 1
    expected_column = 10
    expected_exception = parser.yaml.YAMLError()
    expected_exception.problem_mark = mocker.MagicMock()
    expected_exception.problem_mark.line = expected_line
    expected_exception.problem_mark.column = expected_column

    mocker.patch.object(parser.yaml, "load", side_effect=expected_exception)
    file_open_mock = mocker.patch("builtins.open")
    file_open_mock.read_data = data

    with pytest.raises(Exception,
                       match=r'YAML SyntaxError.*[{}].*[{}].*'.format(expected_line+1, expected_column+1)):
        parser.load_yaml(file_path)

    file_open_mock.assert_called_once_with(file_path, 'r')


def test_schema_error(mocker):
    data = {}
    file_path = "/path/tests"

    mocker.patch.object(parser.yaml, "load", return_value=data)
    file_open_mock = mocker.patch("builtins.open")
    file_open_mock.read_data = data

    with pytest.raises(Exception,  match=r'YAML SchemaError:.*'):
        parser.load_yaml(file_path)

    file_open_mock.assert_called_once_with(file_path, 'r')
