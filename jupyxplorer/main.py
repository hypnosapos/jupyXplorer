import logging
import sys

from traitlets import Unicode
from traitlets.config import Config
from nbconvert.preprocessors import Preprocessor
from nbconvert.exporters import NotebookExporter
import nbformat

from jupyxplorer.parser import load_yml, validate_data, parser_errors


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


class FillName(Preprocessor):
    """A preprocessor to fill the name of a field on some of the cells of a notebook"""

    field   = Unicode(u'field_name', help='name of the field to explore').tag(config=True)

    def preprocess(self, nb, resources):
        self.log.info("I'll add %d as name of the field to explore", self.field)
        for cell in nb.cells:
            cell.source = cell.source.format(self.field)
        return nb, resources


data = load_yml('../sample_metadata.yaml')
if validate_data(data):
    c = Config()
    c.FillName.field = 'acquirer'
    c.NotebookExporter.preprocessors = [FillName]
    c.FillName.enabled = True

    exporter = NotebookExporter(config=c)
    notebook = nbformat.read('../notebooks/numeric.ipynb', as_version=4)

    print(exporter.from_notebook_node(notebook)[0])
elif type(data) is str:
    logger.error("YAMLError: {}".format(data))
else:
    logger.error("SchemaError: your metadata file is incorrect. "
                 "Please, fix the next errors: {}".format(parser_errors(data)))
