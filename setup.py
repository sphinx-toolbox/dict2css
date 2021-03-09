#!/usr/bin/env python
# This file is managed by 'repo_helper'. Don't edit it directly.

# stdlib
import shutil
import sys

# 3rd party
from setuptools import setup

sys.path.append('.')

# this package
from __pkginfo__ import *  # pylint: disable=wildcard-import

setup(
		description="A μ-library for constructing cascading style sheets from Python dictionaries.",
		extras_require=extras_require,
		install_requires=install_requires,
		py_modules=[],
		version=__version__,
		)

shutil.rmtree("dict2css.egg-info", ignore_errors=True)
