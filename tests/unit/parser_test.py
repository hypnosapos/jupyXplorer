import os
import jupyxplorer.parser as parser

import pytest

@pytest.skip
def test_patch(mocker):
    data = "data"
    file_path = "/path/tests"
    file_mock = mocker.MagicMock()
    load_yaml_mock = mocker.patch.object(parser.yaml, 'load', return_value="")

    with mocker.patch("builtins.open", file_mock):
        parser.load_yaml(file_path)

    file_mock.assert_called_with(file_path, 'r')
    load_yaml_mock.assert_called_with(data)
