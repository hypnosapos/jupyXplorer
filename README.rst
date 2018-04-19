jupyXplorer
===========
.. image:: https://circleci.com/gh/hypnosapos/jupyXplorer/tree/master.svg?style=svg
   :target: https://circleci.com/gh/hypnosapos/jupyXplorer/tree/master
   :alt: Build Status
.. image:: https://img.shields.io/pypi/v/jupyxplorer.svg?style=flat-square
   :target: https://pypi.org/project/modeldb-basic
   :alt: Version
.. image:: https://img.shields.io/pypi/pyversions/jupyxplorer.svg?style=flat-square
   :target: https://pypi.org/project/jupyXplorer
   :alt: Python versions
.. image:: https://codecov.io/gh/hypnosapos/jupyXplorer/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/hypnosapos/jupyXplorer
   :alt: Coverage

This project is intended to generate some util notebooks to get data exploration.

It's based on nbconvert and simply offer you a easy way to analise a feature (column) values of a dataset.

Installation
------------

In order to install the utility just use pip:

.. code-block:: bash

    pip install jupyXplorer

We provide you a docker image to get started quickly, take a look at ```` and select the best one fit your needs.


Usage
-----

Before notebook generation take a look at our config file example (tests/e2e/sample_config.yaml).


.. code-block:: bash

    jupyxplorer -c config.yaml -o .output

All notebooks are ready at directory ".output" in the example above.

Once notebooks are generated we can use them in your jupyter to show results of data analysis.
