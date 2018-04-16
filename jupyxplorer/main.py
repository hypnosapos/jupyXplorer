# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from traitlets import Unicode
from traitlets.config import Config
from nbconvert.preprocessors import Preprocessor
from nbconvert.exporters import NotebookExporter
import nbformat

import argparse


class FillName(Preprocessor):
    """A preprocessor to fill the name of a field on some of the cells of a notebook"""

    field   = Unicode(u'field_name', help='name of the field to explore').tag(config=True)

    def preprocess(self, nb, resources):
        self.log.info("I'll add %d as name of the field to explore", self.field)
        for cell in nb.cells:
            cell.source = cell.source.format(self.field)
        return nb, resources


c = Config()
c.FillName.field = 'acquirer'
c.NotebookExporter.preprocessors = [FillName]
c.FillName.enabled = True

exporter = NotebookExporter(config=c)
notebook = nbformat.read('../notebooks/index.ipynb', as_version=4)

print(exporter.from_notebook_node(notebook)[0])


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(prog='jupyxplorer')


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