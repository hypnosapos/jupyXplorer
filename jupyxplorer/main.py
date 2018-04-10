from traitlets import Unicode
from traitlets.config import Config
from nbconvert.preprocessors import Preprocessor
from nbconvert.exporters import NotebookExporter
import nbformat


class FillName(Preprocessor):
    """A preprocessor to fill the name of a field on some of the cells of a notebook"""

    field   = Unicode("field", help="name of the field to explore")
    field.tag(config='True')

    def preprocess(self, nb, resources):
        self.log.info("I'll keep only cells from %d", self.field)
        for cell in nb.cells:
            print(cell.metadata)
            # if cell.metadata.name == "lae":
            #     print("LAENK")
        return nb, resources


c = Config()
c.FillName.field = "acquirer"
c.NotebookExporter.preprocessors = [FillName]

exporter = NotebookExporter(config=c)

notebook = nbformat.read('../notebooks/index.ipynb', as_version=4)

# Process the notebook
print(exporter.from_notebook_node(notebook)[0])
