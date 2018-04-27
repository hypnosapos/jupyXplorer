jupyXplorer
===========
.. image:: https://circleci.com/gh/hypnosapos/jupyXplorer/tree/master.svg?style=svg
   :target: https://circleci.com/gh/hypnosapos/jupyXplorer/tree/master
   :alt: Build Status
.. image:: https://img.shields.io/pypi/v/jupyxplorer.svg?style=flat-square
   :target: https://pypi.org/project/jupyXplorer
   :alt: Version
.. image:: https://img.shields.io/pypi/pyversions/jupyxplorer.svg?style=flat-square
   :target: https://pypi.org/project/jupyXplorer
   :alt: Python versions
.. image:: https://codecov.io/gh/hypnosapos/jupyXplorer/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/hypnosapos/jupyXplorer
   :alt: Coverage

This project aims to generate some util notebooks to get data exploration.

It's based on nbconvert and simply offer you a easy way to analise a feature value (or set of them) of a dataset.

Installation
------------

In order to install the utility just use pip:

.. code-block:: bash

    pip install jupyXplorer

We provide you a docker image to get started quickly, take a look at **hypnosapos/jupyxplorer** at
`dockerhub <https://hub.docker.com/r/hypnosapos/jupyxplorer/>`_ and select the best one fit your needs.


Usage
-----

Before notebook generation take a look at our config file example (tests/e2e/sample_config.yaml).


.. code-block:: bash

    jupyxplorer -c config.yaml -o .output

All notebooks are ready at directory ".output" in the example above.

Once notebooks are generated we can use them in your jupyter to show results of data analysis.

As we said above, you may use a docker container instead:

.. code-block:: bash

   docker run -it -v </path/my_config.yaml>:/tmp/my_config.yaml </path/output>:/tmp/output hypnosapos/jupyxplorer:latest jupyxplorer -c /tmp/my_config.yaml -o /tmp/output


Requirements
------------

You have to put your requirement files on directory ".input". In the config yaml, you have to add filenames only.


Dev
---

The development lifecycle is managed by a **Makefile** and CircleCI, where all steps are executed through docker containers.
Type ``make help`` to see all available commands.

