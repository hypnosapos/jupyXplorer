# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

import os
import pytest

from . import CONFIG_EXAMPLE, OUTPUT_DIR


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
    return CONFIG_EXAMPLE


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

    with pytest.raises(SystemExit) as exc:
        scmd.main(['-c', config, '-o', OUTPUT_DIR])

    load_yaml_mock.assert_called_once_with(config)

    assert 'Unexpected error' in caplog.text
    assert exc.value.code == 1


def test_keyboard_interruptus(scmd, fake_config, mocker, caplog):

    config = 'config.yaml'
    load_yaml_mock = mocker.patch.object(scmd, 'load_yaml', side_effect=KeyboardInterrupt)

    with pytest.raises(SystemExit) as exc:
        scmd.main(['-c', config, '-o', OUTPUT_DIR])

    load_yaml_mock.assert_called_once_with(config)

    assert 'interrupted' in caplog.text
    assert exc.value.code == 2


def test_invalid_document(scmd, mocker, caplog):

    config = 'config.yaml'
    conf = '{·}{.}'
    load_yaml_mock = mocker.patch.object(scmd, 'load_yaml', return_value=conf)

    with pytest.raises(SystemExit) as exc:
        scmd.main(['-c', config, '-o', OUTPUT_DIR])

    load_yaml_mock.assert_called_once_with(config)

    assert 'Unexpected error' in caplog.text
    assert exc.value.code == 1


def test_happy_ending(scmd, correct_config, mocker):

    config = 'config.yaml'
    conf = correct_config
    load_yaml_mock = mocker.patch.object(scmd, 'load_yaml', return_value=conf)

    with pytest.raises(SystemExit) as exc:
        scmd.main(['-c', config, '-o', OUTPUT_DIR])

    load_yaml_mock.assert_called_once_with(config)

    assert os.path.exists(OUTPUT_DIR)
    expected_file_names = ['exploration_{}.ipynb'.format(name) for name in ['num', 'cat']]
    file_names = os.listdir(OUTPUT_DIR)
    assert file_names == expected_file_names
    assert exc.value.code == 0


def test_make_dir(scmd, mocker):
    config = 'config.yaml'
    output_dir = '/path/inexistent'
    conf = correct_config

    mocker.patch.object(scmd, 'load_yaml', return_value=conf)
    make_dirs_mock = mocker.patch.object(scmd.os, "makedirs", side_effect=SystemExit)

    with pytest.raises(SystemExit):
        scmd.main(['-c', config, '-o', output_dir])

    make_dirs_mock.assert_called_once_with(output_dir)
