# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

import jupyxplorer.parser as parser


def test_load_yaml(mocker):
    # Given
    data = "data"
    file_path = "/path/tests"
    expected_result = ''

    mocker.patch.object(parser.yaml, "load", return_value=expected_result)
    file_open_mock = mocker.patch("builtins.open")
    file_open_mock.read_data = data

    # When
    result = parser.load_yaml(file_path)

    file_open_mock.assert_called_once_with(file_path, 'r')

    # Then
    assert result == expected_result
