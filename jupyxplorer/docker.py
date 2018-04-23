import docker


def execute(**kwargs):
    client = docker.from_env()

    volumes ={
        kwargs["output_dir"]: {'bind': '/home/jovyan/.output', 'mode': 'rw'},
        kwargs["input_dir"]: {'bind': '/home/jovyan/.input', 'mode': 'ro'}
    }

    client.containers.run(
        image="jupyter/base-notebook:latest",
        command="jupyter nbconvert"
        " --ExecutePreprocessor.interrupt_on_timeout=True"
        " --ExecutePreprocessor.allow_errors=True"
        " --Application.log_level='INFO'"
        " --ExecutePreprocessor.timeout=300"
        " --execute {}".format(kwargs["output_dir"]),
        volumes=volumes
    )
