#!/usr/bin/env python3
#
#  __init__.py
"""
A μ-library for constructing cascasing style sheets from Python dictionaries.

.. seealso:: `css-parser <https://github.com/ebook-utils/css-parser>`_, which this library builds upon.
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
from contextlib import contextmanager
from typing import IO, Iterator, Mapping, Sequence, Union

# 3rd party
import css_parser  # type: ignore
from domdf_python_tools.words import TAB

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020-2021 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.1.0"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = ["dumps", "dump", "CSSSerializer", "StyleSheet", "em", "make_style", "px", "rem", "Style", "IMPORTANT"]

#: The string ``'important'``.
IMPORTANT = "important"

Style = Mapping[str, Union[Sequence, str, int, None]]
"""
Type annotation representing a style for :func:`~.make_style` and :func:`~.dumps`.

The keys are CSS properties.

The values can be either:

* A :class:`str`, :class:`float` or :py:obj:`None`, giving the value of the property.
* A :class:`tuple` of the property's value (as above) and
  :data:`~.IMPORTANT`, which sets ``!important`` on the property.
"""


def dumps(
		styles: Mapping[str, Style],
		*,
		indent: str = TAB,
		trailing_semicolon: bool = False,
		indent_closing_brace: bool = False,
		minify: bool = False,
		) -> str:
	r"""
	Construct a cascading style sheet from a dictionary.

	:param styles: A mapping of CSS selectors to styles.
	:param indent: The indent to use, such as a tab (``\t``), two spaces or four spaces.
	:param trailing_semicolon:  Whether to add a semicolon to the end of the final property.
	:param indent_closing_brace:
	:param minify: Minify the CSS. Overrides all other options.

	:return: The style sheet as a string.
	"""

	serializer = CSSSerializer(
			indent=indent,
			trailing_semicolon=trailing_semicolon,
			indent_closing_brace=indent_closing_brace,
			minify=minify,
			)

	with serializer.use():
		sheet = StyleSheet()

		for selector, style in styles.items():
			sheet.add_style(selector, style)

		stylesheet = sheet.tostring()

	if not serializer.minify:
		stylesheet = stylesheet.replace('}', "}\n")

	return stylesheet


def dump(
		styles: Mapping[str, Style],
		fp: IO,
		*,
		indent: str = TAB,
		trailing_semicolon: bool = False,
		indent_closing_brace: bool = False,
		minify: bool = False,
		):
	r"""
	Construct a cascading style sheet from a dictionary and write it to ``fp``.

	:param styles: A mapping of CSS selectors to styles.
	:param fp: An open file handle.
	:param indent: The indent to use, such as a tab (``\t``), two spaces or four spaces.
	:param trailing_semicolon:  Whether to add a semicolon to the end of the final property.
	:param indent_closing_brace:
	:param minify: Minify the CSS. Overrides all other options.
	"""

	css = dumps(
			styles,
			indent=indent,
			trailing_semicolon=trailing_semicolon,
			indent_closing_brace=indent_closing_brace,
			minify=minify,
			)

	fp.write(css)


class CSSSerializer(css_parser.CSSSerializer):
	r"""
	Serializes a :class:`~.StyleSheet` and its parts.

	This controls the formatting of the style sheet.

	:param indent: The indent to use, such as a tab (``\t``), two spaces or four spaces.
	:param trailing_semicolon:  Whether to add a semicolon to the end of the final property.
	:param indent_closing_brace:
	:param minify: Minify the CSS. Overrides all other options.
	"""

	def __init__(
			self,
			*,
			indent: str = TAB,
			trailing_semicolon: bool = False,
			indent_closing_brace: bool = False,
			minify: bool = False,
			):
		super().__init__()
		self.indent = str(indent)
		self.trailing_semicolon = trailing_semicolon
		self.indent_closing_brace = indent_closing_brace
		self.minify = minify

	def reset_style(self) -> None:
		"""
		Reset the serializer to its default style.
		"""

		# Reset CSS Parser to defaults
		self.prefs.useDefaults()

		if self.minify:
			self.prefs.useMinified()

		else:
			# Formatting preferences
			self.prefs.omitLastSemicolon = not self.trailing_semicolon
			self.prefs.indentClosingBrace = self.indent_closing_brace
			self.prefs.indent = self.indent

	@contextmanager
	def use(self) -> Iterator:
		"""
		Contextmanager to use this serializer for the scope of the ``with`` block.
		"""

		# if css_parser.ser is self:
		# 	yield
		# 	return
		#
		current_serializer = css_parser.ser
		self.reset_style()

		try:
			css_parser.ser = self
			yield

		finally:
			css_parser.ser = current_serializer


class StyleSheet(css_parser.css.CSSStyleSheet):
	"""
	Represents a CSS style sheet.
	"""

	def __init__(self):
		super().__init__(validating=False)

	def add(self, rule: css_parser.css.CSSRule) -> int:
		"""
		Add the ``rule`` to the style sheet.

		:param rule:
		:type rule: :class:`css_parser.css.CSSRule`
		"""

		return super().add(rule)

	def add_style(
			self,
			selector: str,
			styles: Style,
			) -> None:
		"""
		Add a style to the style sheet.

		:param selector:
		:param styles:
		"""

		self.add(make_style(selector, styles))

	def tostring(self) -> str:
		"""
		Returns the style sheet as a string.
		"""

		return self.cssText.decode("UTF-8")


def make_style(selector: str, styles: Style) -> css_parser.css.CSSStyleRule:
	"""
	Create a CSS Style Rule from a dictionary.

	:param selector:
	:param styles:

	:rtype: :class:`css_parser.css.CSSStyleRule`
	"""

	style = css_parser.css.CSSStyleDeclaration()
	style.validating = False

	for name, properties in styles.items():
		if isinstance(properties, Sequence) and not isinstance(properties, str):
			style[name] = tuple(str(x) for x in properties)
		else:
			style[name] = str(properties)

	return css_parser.css.CSSStyleRule(selectorText=selector, style=style)


def px(val: Union[int, float, str]) -> str:
	"""
	Helper function to format a number as a value in pixels.

	:param val:
	"""

	return f"{val}px"


def em(val: Union[int, float, str]) -> str:
	"""
	Helper function to format a number as a value in em.

	:param val:
	"""

	return f"{val}em"


def rem(val: Union[int, float, str]) -> str:
	"""
	Helper function to format a number as a value in rem.

	:param val:
	"""

	return f"{val}rem"
