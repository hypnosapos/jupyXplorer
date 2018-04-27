# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

import jupyxplorer.docker as jupydocker


def test_load_yaml(mocker):

    input_dir = 'input_dir',
    output_dir = 'output_dir'

    docker_client_mock = mocker.MagicMock()
    docker_containers_mock = mocker.MagicMock()
    docker_run_mock = mocker.MagicMock(return_value=None)
    docker_client_mock.containers = docker_containers_mock
    docker_client_mock.containers.run = docker_run_mock

    mocker.patch.object(jupydocker.docker, "from_env", return_value=docker_client_mock)

    jupydocker.execute(input_dir, output_dir)

    docker_run_mock.assert_called_once_with(
        image=jupydocker.DOCKER_IMAGE,
        command=jupydocker.DOCKER_COMMAND,
        volumes={
            input_dir: jupydocker.DOCKER_VOLUMES['input_dir'],
            output_dir: jupydocker.DOCKER_VOLUMES['output_dir']
        }
    )
