
"""

Auto Explorer setup

"""
from setuptools import setup, find_packages
import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(BASE_DIR, 'README.rst')) as f:
    README = f.read()

with open(os.path.join(BASE_DIR, 'requirements.txt')) as f:
    requirements = f.read().splitlines()

setup(name='jupyXplorer',
      python_requires='>=3.5',
      version="0.0.3",
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
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "docs"]),
      include_package_data=True,
      install_requires=requirements,
      entry_points={
          'console_scripts': [
              "jupyxplorer = jupyxplorer.main:main"
          ]
      },
      zip_safe=False)
