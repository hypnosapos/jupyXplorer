# Copyright 2018 BBVA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""

Auto Explorer setup

"""
from setuptools import setup, find_packages
import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(BASE_DIR, 'README.rst')) as f:
    README = f.read()

setup(name='jupyXplorer',
      python_requires='>=3.5',
      version='1.0.0',
      description="jupyXplorer: notebooks generator from data",
      license="MIT",
      long_description=README,
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Scientific/Engineering :: Information Analysis'
      ],
      author='Hypnosapos',
      url='https://github.com/hypnosapos/jupyXplorer',
      packages=find_packages(exclude=["tests", "docs"]),
      include_package_data=True,
      zip_safe=False)
