# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

import argparse
import logging
import os
import sys

import nbformat

from nbconvert.exporters import NotebookExporter
from traitlets.config import Config

from .parser import load_yaml
from .processors import FillName

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def main(argv=sys.argv[1:]):
    try:
        parser = argparse.ArgumentParser(prog='jupyxplorer')
        parser.add_argument("-c", '--config-file',
                            default='config.yaml',
                            required=True,
                            type=load_yaml,
                            help='Config file. Defaults to config.yaml')
        parser.add_argument("-o", '--output-dir',
                            default='.output',
                            required=False,
                            help='Directory where output files will be saved to.')

        args = parser.parse_args(argv)
        data = args.config_file
        output_dir = args.output_dir or ".output"

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for field in data["fields"]:
            c = Config()
            c.FillName.field = field["name"]
            c.NotebookExporter.preprocessors = [FillName]
            c.FillName.enabled = True

            exporter = NotebookExporter(config=c)
            notebook = nbformat.read(os.path.join(BASE_DIR,
                                                  'notebooks/{}.ipynb'.format(field["type"])), as_version=4)
            with open('{}/exploration_{}.ipynb'.format(output_dir, field["type"]), 'w') as nbfile:
                nbfile.write(exporter.from_notebook_node(notebook)[0])

    except KeyboardInterrupt:
        logger.warning("... jupyxplorer command was interrupted")
        sys.exit(2)
    except Exception as ex:
        logger.error('Unexpected error: %s' % ex)
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
