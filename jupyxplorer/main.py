# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

import argparse
import logging
import os
import sys

import nbformat

from nbconvert.exporters import NotebookExporter
from traitlets.config import Config

from .parser import load_yml, validate_data, parser_errors
from .processors import FillName

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
LOG = logging.getLogger(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(prog='jupyxplorer')
    parser.add_argument("-c", '--config-file',
                        default='config.yaml',
                        help='Config file. Defaults to config.yaml')
    args = parser.parse_args(argv)
    data = load_yml(args.config_file)
    if validate_data(data):
        for field in data["fields"]:
            c = Config()
            c.FillName.field = field["name"]
            c.NotebookExporter.preprocessors = [FillName]
            c.FillName.enabled = True

            exporter = NotebookExporter(config=c)
            notebook = nbformat.read(os.path.join(BASE_DIR,
                                                  '../notebooks/{}.ipynb'.format(field["type"])), as_version=4)

            print(exporter.from_notebook_node(notebook)[0])
    elif type(data) is str:
        LOG.error("YAMLError: {}".format(data))
    else:
        LOG.error("SchemaError: your metadata file is incorrect. "
                  "Please, fix the next errors: {}".format(parser_errors(data)))


if __name__ == "__main__":

    try:
        main(sys.argv[1:])

    except KeyboardInterrupt:
        LOG.warning("... jupyxplorer command was interrupted")
        sys.exit(2)
    except Exception as ex:
        LOG.error('Unexpected error: %s' % ex)
        sys.exit(1)
    sys.exit(0)
