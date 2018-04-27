# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

import docker

DOCKER_IMAGE = "jupyter/pyspark-notebook:latest"

DOCKER_COMMAND = "jupyter nbconvert" \
    " --ExecutePreprocessor.interrupt_on_timeout=True" \
    " --ExecutePreprocessor.allow_errors=True" \
    " --Application.log_level='INFO'" \
    " --ExecutePreprocessor.timeout=300" \
    " --execute /home/jovyan/*.ipynb"

DOCKER_VOLUMES = {
    "output_dir": {'bind': '/home/jovyan', 'mode': 'rw'},
    "input_dir": {'bind': '/home/jovyan/work', 'mode': 'ro'}
}


def execute(input_dir, output_dir):

    client = docker.from_env()

    volumes = {
        output_dir: DOCKER_VOLUMES['output_dir'],
        input_dir: DOCKER_VOLUMES['input_dir']
    }

    client.containers.run(
        image=DOCKER_IMAGE,
        command=DOCKER_COMMAND,
        volumes=volumes
    )
