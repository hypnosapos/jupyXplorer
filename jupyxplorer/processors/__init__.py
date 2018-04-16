# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from nbconvert.preprocessors import Preprocessor
from traitlets import Unicode


class FillName(Preprocessor):
    """A preprocessor to fill the name of a field on some of the cells of a notebook"""

    field = Unicode(u'field_name', help='name of the field to explore').tag(config=True)

    def preprocess(self, nb, resources):
        self.log.info("I'll add {} as name of the field to explore".format(self.field))
        for cell in nb.cells:
            cell.source = cell.source.format(self.field)
        return nb, resources
