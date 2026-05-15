#!/usr/bin/env python3
#
#  __init__.py
"""
A μ-library for constructing cascasing style sheets from Python dictionaries.
"""
#
#  Copyright © 2020-2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
from io import TextIOBase
from typing import IO, Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Union

# 3rd party
import tinycss2  # type: ignore[import-untyped]
import tinycss2.ast  # type: ignore[import-untyped]
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.typing import PathLike
from domdf_python_tools.words import TAB

# this package
from dict2css.helpers import em, px, rem  # noqa: F401
from dict2css.serializer import CSSSerializer

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020-2026 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.5.0"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = [
		"IMPORTANT",
		"Style",
		"dumps",
		"dump",
		"loads",
		"load",
		]

# TODO: allow int indent like json.dumps etc.

IMPORTANT = "important"
"""
The string ``'important'``.

.. latex:vspace:: 10px
"""

# Property = Union[Tuple[Union[str, int, None], str], str, int, None]
Property = Union[Sequence, str, int, float, None]

Style = Mapping[str, Property]
"""
Type annotation representing a style for :func:`~.dumps` and :func:`~.dump`.

The keys are CSS properties.

The values can be either:

* A :class:`str`, :class:`float` or :py:obj:`None`, giving the value of the property.
* A :class:`tuple` of the property's value (as above) and the priority
  such as :data:`~.IMPORTANT` (which sets ``!important`` on the property).
"""


def dumps(
		styles: Mapping[str, Union[Style, Mapping]],
		*,
		indent: str = TAB,
		trailing_semicolon: Optional[bool] = None,
		indent_closing_brace: bool = False,
		minify: bool = False,
		sort_keys: bool = False,
		check_circular: bool = True,
		) -> str:
	r"""
	Construct a cascading style sheet from a dictionary.

	``styles`` is a mapping of CSS selector strings to styles, which map property names to their values:

	.. code-block:: python

		styles = {".wy-nav-content": {"max-width": (px(1200), IMPORTANT)}}
		print(dumps(styles))

	.. code-block:: css

		.wy-nav-content {
			max-width: 1200px !important
		}

	See the :py:obj:`~.Style` object for more information on the layout.

	The keys can also be media at-rules, with the values mappings of property names to their values:

	.. code-block:: python

		styles = {
			"@media screen and (min-width: 870px)": {
				".wy-nav-content": {"max-width": (px(1200), IMPORTANT)},
				},
			}
		print(dumps(styles))

	.. code-block:: css

		@media screen and (min-width: 870px) {
			.wy-nav-content {
				max-width: 1200px !important
			}
		}

	:param styles: A mapping of CSS selectors to styles.
	:param indent: The indent to use, such as a tab (``\t``), two spaces or four spaces.
	:param trailing_semicolon:  Whether to add a semicolon to the end of the final property.
	:param indent_closing_brace:
	:param minify: Minify the CSS. Overrides all other options.
	:param sort_keys: Sort dictionary keys alphabetically.
	:param check_circular: Check for circular references.

	:return: The style sheet as a string.

	.. versionchanged:: 0.2.0  Added support for media at-rules.
	.. versionchanged:: 0.5.0  New implementation. Output may differ slightly from previous css-parser based one.
	"""

	serializer = CSSSerializer(
			indent=indent,
			trailing_semicolon=trailing_semicolon,
			indent_closing_brace=indent_closing_brace,
			minify=minify,
			sort_keys=sort_keys,
			check_circular=check_circular,
			)

	css = serializer.encode(styles).rstrip()

	if css:
		return css + '\n'
	else:
		return ''


def dump(
		styles: Mapping[str, Union[Style, Mapping]],
		fp: Union[PathLike, IO],
		*,
		indent: str = TAB,
		trailing_semicolon: Optional[bool] = None,
		indent_closing_brace: bool = False,
		minify: bool = False,
		sort_keys: bool = False,
		check_circular: bool = True,
		) -> None:
	r"""
	Construct a style sheet from a dictionary and write it to ``fp``.

	.. code-block:: python

		styles = {".wy-nav-content": {"max-width": (px(1200), IMPORTANT)}}
		dump(styles, ...)

	.. code-block:: css

		.wy-nav-content {
			max-width: 1200px !important
		}

	See the :py:obj:`~.Style` object for more information on the layout.

	.. latex:clearpage::

	The keys can also be media at-rules, with the values mappings of property names to their values:

	.. code-block:: python

		styles = {
			"@media screen and (min-width: 870px)": {
				".wy-nav-content": {"max-width": (px(1200), IMPORTANT)},
				},
			}
		dump(styles, ...)

	.. code-block:: css

		@media screen and (min-width: 870px) {
			.wy-nav-content {
				max-width: 1200px !important
			}
		}

	:param styles: A mapping of CSS selectors to styles.
	:param fp: An open file handle, or the filename of a file to write to.
	:param indent: The indent to use, such as a tab (``\t``), two spaces or four spaces.
	:param trailing_semicolon:  Whether to add a semicolon to the end of the final property.
	:param indent_closing_brace:
	:param minify: Minify the CSS. Overrides all other options.
	:param sort_keys: Sort dictionary keys alphabetically.
	:param check_circular: Check for circular references.

	.. versionchanged:: 0.2.0

		* ``fp`` now accepts :py:obj:`domdf_python_tools.typing.PathLike` objects,
		  representing the path of a file to write to.
		* Added support for media at-rules.

	.. versionchanged:: 0.5.0  New implementation. Output may differ slightly from previous css-parser based one.
	"""

	css = dumps(
			styles,
			indent=indent,
			trailing_semicolon=trailing_semicolon,
			indent_closing_brace=indent_closing_brace,
			sort_keys=sort_keys,
			check_circular=check_circular,
			minify=minify,
			)

	if isinstance(fp, TextIOBase):
		fp.write(css)
	else:
		PathPlus(fp).write_clean(css)


def loads(styles: str) -> MutableMapping[str, MutableMapping[str, Any]]:
	r"""
	Parse a style sheet and return its dictionary representation.

	.. versionadded:: 0.2.0
	.. versionchanged:: 0.5.0  New implementation. Output may differ slightly from previous css-parser based one.

	:param styles:

	:return: The style sheet as a dictionary.

	.. latex:clearpage::
	"""

	stylesheet = tinycss2.parse_blocks_contents(styles, skip_comments=True, skip_whitespace=True)

	styles_dict: MutableMapping[str, MutableMapping[str, Any]] = {}

	def parse_style(style: List[tinycss2.ast.Node]) -> MutableMapping[str, Property]:
		style_dict: Dict[str, Property] = {}

		prop: Union[tinycss2.ast.ParseError, tinycss2.ast.Declaration]
		for prop in tinycss2.parse_declaration_list(style, skip_comments=True, skip_whitespace=True):
			if isinstance(prop, tinycss2.ast.ParseError):
				raise ValueError(prop)

			if prop.important:
				style_dict[prop.name.strip()] = (_serialize(prop.value), IMPORTANT)
			else:
				style_dict[prop.name.strip()] = _serialize(prop.value)

		return style_dict

	rule: tinycss2.ast.Node
	for rule in stylesheet:
		if isinstance(rule, tinycss2.ast.QualifiedRule):
			styles_dict[_serialize(rule.prelude)] = parse_style(rule.content)

		elif isinstance(rule, tinycss2.ast.AtRule):
			at_rule_styles = styles_dict[f"@{rule.at_keyword} {_serialize(rule.prelude)}"] = {}

			for child in tinycss2.parse_blocks_contents(rule.content, skip_comments=True, skip_whitespace=True):
				at_rule_styles[_serialize(child.prelude)] = parse_style(child.content)

		else:
			raise NotImplementedError(rule)

	return styles_dict


def _serialize(nodes: Iterable[tinycss2.ast.Node]) -> str:
	return tinycss2.serialize(nodes).strip()


def load(fp: Union[PathLike, IO]) -> MutableMapping[str, MutableMapping[str, Any]]:
	r"""
	Parse a cascading style sheet from the given file and return its dictionary representation.

	.. versionadded:: 0.2.0
	.. versionchanged:: 0.5.0  New implementation. Output may differ slightly from previous css-parser based one.

	:param fp: An open file handle, or the filename of a file to write to.

	:return: The style sheet as a dictionary.
	"""

	if isinstance(fp, TextIOBase):
		styles = fp.read()
	else:
		styles = PathPlus(fp).read_text()

	return loads(styles)
