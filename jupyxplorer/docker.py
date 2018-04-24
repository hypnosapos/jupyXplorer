import docker


def execute(**kwargs):
    client = docker.from_env()

    con_out_dir = '/home/jovyan'

    volumes = {
        kwargs["output_dir"]: {'bind': con_out_dir, 'mode': 'rw'},
        kwargs["input_dir"]: {'bind': '/home/jovyan/work', 'mode': 'ro'}
    }

    client.containers.run(
        image="jupyter/pyspark-notebook:latest",
        command="jupyter nbconvert"
        " --ExecutePreprocessor.interrupt_on_timeout=True"
        " --ExecutePreprocessor.allow_errors=True"
        " --Application.log_level='INFO'"
        " --ExecutePreprocessor.timeout=300"
        " --execute {}/*.ipynb".format(con_out_dir),
        volumes=volumes
    )
