#########
dict2css
#########

.. start short_desc

.. documentation-summary::
	:meta:

.. end short_desc

.. start shields

.. only:: html

	.. list-table::
		:stub-columns: 1
		:widths: 10 90

		* - Docs
		  - |docs| |docs_check|
		* - Tests
		  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
		* - PyPI
		  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
		* - Anaconda
		  - |conda-version| |conda-platform|
		* - Activity
		  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
		* - QA
		  - |codefactor| |actions_flake8| |actions_mypy|
		* - Other
		  - |license| |language| |requires|

	.. |docs| rtfd-shield::
		:project: dict2css
		:alt: Documentation Build Status

	.. |docs_check| actions-shield::
		:workflow: Docs Check
		:alt: Docs Check Status

	.. |actions_linux| actions-shield::
		:workflow: Linux
		:alt: Linux Test Status

	.. |actions_windows| actions-shield::
		:workflow: Windows
		:alt: Windows Test Status

	.. |actions_macos| actions-shield::
		:workflow: macOS
		:alt: macOS Test Status

	.. |actions_flake8| actions-shield::
		:workflow: Flake8
		:alt: Flake8 Status

	.. |actions_mypy| actions-shield::
		:workflow: mypy
		:alt: mypy status

	.. |requires| image:: https://dependency-dash.repo-helper.uk/github/sphinx-toolbox/dict2css/badge.svg
		:target: https://dependency-dash.repo-helper.uk/github/sphinx-toolbox/dict2css/
		:alt: Requirements Status

	.. |coveralls| coveralls-shield::
		:alt: Coverage

	.. |codefactor| codefactor-shield::
		:alt: CodeFactor Grade

	.. |pypi-version| pypi-shield::
		:project: dict2css
		:version:
		:alt: PyPI - Package Version

	.. |supported-versions| pypi-shield::
		:project: dict2css
		:py-versions:
		:alt: PyPI - Supported Python Versions

	.. |supported-implementations| pypi-shield::
		:project: dict2css
		:implementations:
		:alt: PyPI - Supported Implementations

	.. |wheel| pypi-shield::
		:project: dict2css
		:wheel:
		:alt: PyPI - Wheel

	.. |conda-version| image:: https://img.shields.io/conda/v/domdfcoding/dict2css?logo=anaconda
		:target: https://anaconda.org/domdfcoding/dict2css
		:alt: Conda - Package Version

	.. |conda-platform| image:: https://img.shields.io/conda/pn/domdfcoding/dict2css?label=conda%7Cplatform
		:target: https://anaconda.org/domdfcoding/dict2css
		:alt: Conda - Platform

	.. |license| github-shield::
		:license:
		:alt: License

	.. |language| github-shield::
		:top-language:
		:alt: GitHub top language

	.. |commits-since| github-shield::
		:commits-since: v0.3.0.post1
		:alt: GitHub commits since tagged version

	.. |commits-latest| github-shield::
		:last-commit:
		:alt: GitHub last commit

	.. |maintained| maintained-shield:: 2024
		:alt: Maintenance

	.. |pypi-downloads| pypi-shield::
		:project: dict2css
		:downloads: month
		:alt: PyPI - Downloads

.. end shields

``dict2css`` provides an API similar to the :mod:`json` and
toml_ modules, with :func:`~.dump` and :func:`~.load` functions.
The :func:`~.dump` function takes a mapping of `CSS selectors`_
to mappings of CSS properties.
Each property value may, optionally, be a two-element tuple containing the value and the string "important".
The :func:`~.load` function returns a mapping with the same structure.

.. _json: https://docs.python.org/3/library/json.html
.. _toml: https://github.com/uiri/toml/
.. _CSS selectors: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors


Installation
---------------

.. start installation

.. installation:: dict2css
	:pypi:
	:github:
	:anaconda:
	:conda-channels: conda-forge, domdfcoding

.. end installation

Contents
-----------

.. html-section::

.. toctree::
	:hidden:

	Home<self>

.. toctree::
	:maxdepth: 3
	:glob:

	api/dict2css
	api/*
	changelog

.. sidebar-links::
	:caption: Links
	:github:
	:pypi: dict2css

	Contributing Guide <https://contributing-to-sphinx-toolbox.readthedocs.io/en/latest/>
	Source
	license

.. start links

.. only:: html

	View the :ref:`Function Index <genindex>` or browse the `Source Code <_modules/index.html>`__.

	:github:repo:`Browse the GitHub Repository <sphinx-toolbox/dict2css>`

.. end links
