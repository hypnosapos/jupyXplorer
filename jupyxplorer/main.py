# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from traitlets import Unicode
from traitlets.config import Config
from nbconvert.preprocessors import Preprocessor
from nbconvert.exporters import NotebookExporter
import nbformat

from .processors import FillName
import argparse


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(prog='jupyxplorer')

    c = Config()
    c.FillName.field = 'acquirer'
    c.NotebookExporter.preprocessors = [FillName]
    c.FillName.enabled = True

    exporter = NotebookExporter(config=c)
    notebook = nbformat.read('../notebooks/index.ipynb', as_version=4)

    print(exporter.from_notebook_node(notebook)[0])


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