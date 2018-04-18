# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

import os
import pytest


@pytest.fixture
def scmd():

    import jupyxplorer.main as shell_cmd
    return shell_cmd


@pytest.fixture
def fake_config():
    data = {'col1': [1, 2, 3]}
    return data


@pytest.fixture
def correct_config():
    data = {
        "dataset": "path/to/json",
        "fields": [
            {
                "name": "field1",
                "type": "num"
            },
            {
                "name": "field2",
                "type": "cat"
            }
        ]
    }
    return data


def test_help(scmd, capsys):

    with pytest.raises(SystemExit) as se:
        scmd.main(['-h'])

    assert se.value.code == 0

    out, _ = capsys.readouterr()
    assert out.startswith('usage:') and 'optional arguments:' in out


def test_default_required_args(scmd, capsys):

    with pytest.raises(SystemExit) as se:
        scmd.main([])

    assert se.value.code == 2

    _, err = capsys.readouterr()
    assert "error: the following arguments are required: -c/--config-file" in err


def test_schema_validation_yaml(scmd, fake_config, mocker, caplog):

    config = 'config.yaml'
    conf = fake_config
    load_yaml_mock = mocker.patch.object(scmd, 'load_yaml', return_value=conf)
    validate_data_mock = mocker.patch.object(scmd, 'validate_data', return_value=False)

    with pytest.raises(SystemExit) as exc:
        scmd.main(['-c', config])

    load_yaml_mock.assert_called_once_with(config)
    validate_data_mock.assert_called_once_with(conf)

    assert 'SchemaError' in caplog.text
    assert exc.value.code == 1


def test_keyboard_interruptus(scmd, fake_config, mocker, caplog):

    config = 'config.yaml'
    conf = fake_config
    load_yaml_mock = mocker.patch.object(scmd, 'load_yaml', return_value=conf)
    validate_data_mock = mocker.patch.object(scmd, 'validate_data', side_effect=KeyboardInterrupt)

    with pytest.raises(SystemExit) as exc:
        scmd.main(['-c', config])

    load_yaml_mock.assert_called_once_with(config)
    validate_data_mock.assert_called_once_with(conf)

    assert 'interrupted' in caplog.text
    assert exc.value.code == 2


def test_yaml_error(scmd, mocker, caplog):

    config = 'config.yaml'
    conf = '{·}{.}'
    load_yaml_mock = mocker.patch.object(scmd, 'load_yaml', return_value=conf)
    validate_data_mock = mocker.patch.object(scmd, 'validate_data', return_value=False)

    with pytest.raises(SystemExit) as exc:
        scmd.main(['-c', config])

    load_yaml_mock.assert_called_once_with(config)
    validate_data_mock.assert_called_once_with(conf)

    assert 'YAMLError' in caplog.text
    assert exc.value.code == 1


def test_happy_ending(scmd, correct_config, mocker):

    config = 'config.yaml'
    conf = correct_config
    output_dir = '.output-test'
    load_yaml_mock = mocker.patch.object(scmd, 'load_yaml', return_value=conf)
    validate_data_mock = mocker.patch.object(scmd, 'validate_data', return_value=True)

    with pytest.raises(SystemExit) as exc:
        scmd.main(['-c', config, '-o', output_dir])

    load_yaml_mock.assert_called_once_with(config)
    validate_data_mock.assert_called_once_with(conf)

    assert os.path.exists(output_dir)
    expected_file_names = ['exploration_{}.ipynb'.format(name) for name in ['num', 'cat']]
    file_names = os.listdir(output_dir)
    assert file_names == expected_file_names
    assert exc.value.code == 0
