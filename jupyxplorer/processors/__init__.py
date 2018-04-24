# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from nbconvert.preprocessors import Preprocessor
from traitlets import List, Dict
import nbformat as nbf


class Formatter(Preprocessor):
    """A preprocessor to fill the name of a field on some of the cells of a notebook"""

    params = Dict(help='Values pass to format strings to').tag(config=True)

    def preprocess(self, nb, resources):
        self.log.info("I'll add {} as name of the field to explore".format(self.params))
        for cell in nb.cells:
            cell.source = cell.source.format(
                **self.params
            )

        return nb, resources


class InstallRequirements(Preprocessor):
    """A preprocessor to add the installation of requirements at the beginning of the notebooks."""

    requirements = List([], help='list with needed requirement files').tag(config=True)

    def preprocess(self, nb, resources):
        self.log.info("I'll add requirement installation in the notebook.")
        if self.requirements is not []:
            new_cell = nbf.v4.new_code_cell(
                source="!pip install%s" % ''.join([" -r %s" % i for i in self.requirements]))
            nb.cells.insert(2, nbf.v4.new_markdown_cell(source="### Install requirements"))
            nb.cells.insert(3, new_cell)

        return nb, resources
